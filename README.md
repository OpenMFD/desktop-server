OpenMFD Desktop Server
======================

This project is the MFD server that will be responsible for taking in any requests from the UI and running them on the
host machine.

Supported operating systems: Windows and macOS. Linux probably works, but I don't intend on testing it there. The only
reason macOS is supported is because it makes life easier for me as I'm building the UI on macOS.

## Running for development purposes

Note: This assumes you have at least Python 3.7 installed. If your Python3 binary is separate (such as `python3` update 
the first command accordingly)

### On macOS/Linux:

Setup Python venv:

```bash
$ python -m venv venv
```

Active the environment:

```bash
$ source venv/bin/activate
```

Install dependencies:

```bash
$ pip install -r requirements.txt
```

Run dev server:

```bash
$ FLASK_ENV=development FLASK_APP=mfdserver flask run --host=0.0.0.0 --port=6789
```

Make sure you update the IP in the UI project with your local one so that it can connect if you're running it from a
different device on the network.

## Security Design

_Before you read more into this, until this message is removed, this part is WIP and may not be fully implemented or 
documented._

With something like this you do find yourself ending up with a virtual remote keyboard on your machine. So it's 
imperative that we get security of an app like this to be the best it can be.

1. Use and enforce browser SSL.

   This is so that we can offload much of the potential attack vectors from our code 
   into the browser. It might mean teaching the user how to bypass invalid ssl warnings, but the end result is a much 
   safer environment, so I think this is worth the trouble. 

2. No user should have the ability to set a shared secret of any kind. 
   
   This part goes in tandem with 1., as letting the user have the ability to deal with this opens up the vector of 
   brute forcing weak secrets.
   
3. The clients and servers should have have their own ID (UUID v4).

   UUID's are a generally a safe way of being able to generate a unique ID without the involvement of the server. However
   the risk of one being generated by a remote attacker that matches the either a client or a server is extremely low.
   
   Server: 
   
   On first startup the server will generate an id and persist it to disk. This will be what it broadcasts to clients.
   
   If this ID changes then no client should trust the server.
   
   --
   
   Client:
   
   On first startup the client will generate an id and persist it to localstorage. This will be what it broadcasts to the server.
   
   If this ID changes then the server should no longer trust the client.
   
   Possible Issues:
   
   If the server changes IPs often the user will be forced to revalidate a new client.
      
   Possible Solutions:
   - Host the app on a domain, so that it retains it can retain local storage.
     
     This solution would mean that the server should be configured to allow cors to whatever domain
     this is allowed on. (WebSockets don't have support for cors, but authentication will deal with this side as a 
     mitigating factor)

4. Authentication Flow
  
   Diagram:
   
   ```
                          Client                          Server                          
                             │                              │                             
   ┌──────────────────────┐  ├──────────GET /info───────────▶                             
   │   The client will    │  ◀ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─│                             
   │validate if the server│  │                              │                             
   │is known, if it is it │  ├───▶──────────────┐           │                             
   │will later communicate│  │   │  Validation  │           │                             
   │ its id, otherwise if │  ◀───┴──────────────┘           │                             
   │   it isn't it will   │  │                              │ ┌──────────────────────────┐
   │inform the user, and a│  ├──────────POST /auth──────────▶ │ The server will validate │
   │    new ID will be    │  │                              │ │ the communicated client  │
   │      generated.      │  │           ┌──────────────◀───┤ │ id, if it is known, then │
   └──────────────────────┘  │           │  Validation  │   │ │ it will response. If not │
                             │           └──────────────┴───▶ │ the user will be alerted │
                             │                              │ │and be asked if it should │
                             │◀ ─ ─ ─ ─ access token─ ─ ─ ─ ┤ │  give permission to the  │
                             │                              │ │    connecting client.    │
                             │                              │ └──────────────────────────┘
                             │                              │ ┌──────────────────────────┐
                             │           Socket.IO          │ │The access token should be│
                             ├─────────connection /w────────▶ │ valid, other wise a 403  │
                             │         access token         │ │ will be responded with.  │
                             │                              │ └──────────────────────────┘
                             │◀ ─ ─ ─Socket details ─ ─ ─ ─ ┤                             
                                                                                          
   ```

   Server Notes:  
    - Expose a `GET /info` endpoint that will include the server ID
    - Expose a `POST /authorise` endpoint that a client can exchange its client id for a time limited access token.
    - WebSockets will require this token in order to be instantiated.
    - Occasionally the server should broadcast a new token to connected clients so they can be rotated.
   
   Client Notes:
    - Client will fetch server info via `GET /info` and validate the server ID against a known one, if stored.
      - Should the ID fail to match, the user should be warned and if the user overrides it, then a new client id must
        be generated so that we don't leak the old one.
    - Any attempts to reauthenticate after a disconnection occurs should go through the same process as the above.
      The client should not trust that the server is still the same. 
