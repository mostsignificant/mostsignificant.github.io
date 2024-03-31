---
layout: post
title: "How To Build A Simple But Efficient Key-Value-Store With Rust And Actix"
date: 2023-10-09 19:00:00 +0200
categories:
comments: true
published: true
excerpt: |
  Rust and the actix framework are predestined for building a key-value-store with just a few simple lines of code. This
  small tool will be purely in-memory and support setting, getting and deleting keys via HTTP.
image_url: /assets/images/unsplash/edgar-chaparro-d9UQsgHL2Ug-unsplash.jpg
image_description: |
  Photo by [Edgar Chaparro](https://unsplash.com/@echaparro?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText)
  on [Unsplash](https://unsplash.com/photos/d9UQsgHL2Ug?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText)
---

The code for this article can found on my [GitHub](https://github.com/mostsignificant/iowa).

## What Is A Key-Value-Store?

One of the simplest forms of a database is a key-value-store. It should be one of the first things being taught in
database courses. A simple version can be implemented relatively quickly and be a quick win for any developers that are
getting started.

> A key–value database, or key–value store, is a data storage paradigm designed for storing, retrieving, and managing
> associative arrays, and a data structure more commonly known today as a dictionary or hash table.
>
> **- [wikipedia](https://en.wikipedia.org/wiki/Key–value_database)**

To oversimplify things, one could say a filesystem is a key-value-store: the paths and file names are the keys and the
documents are the values. The mentioned data structures in the wikipedia article should be available in 99.9% of
mainstream programming languages and a simple API can be implemented quickly: command line, HTTP endpoints, etc.

## Rust And Actix

Rust is the perfect close-to-the-metal language for implementing anything database related: fast and secure.
Traditionally, a lot of databases are built in C or C++ or both. Will Rust replace either of these two languages? Nobody
knows. There are some databases already implemented in Rust, for example [SurrealDB](https://surrealdb.com). For our use
case, the language is a perfect fit.

[Actix](https://actix.rs) is actually an actor framework. This means the framework is built upon so-called actors, which
are components that can send messages to each other and process those asynchronously. What is the advantage of this? You
do not need lock-based synchronization anymore. This makes it a perfect fit for handling HTTP requests. The web
implementation of the actix framework is called [actix-web](https://github.com/actix/actix-web) (surprise, surprise).

## The Design

The data will be stored solely in memory. This means no persistence in between restarts. A data storage mechanism to
store the data on disk is an optional task left to the reader to implement. There are a lot of options for data storage
engines in Rust, for example [sled](https://github.com/spacejam/sled) or [AgateDB](https://github.com/tikv/agatedb). Or
you just do it from [scratch](https://rustmagazine.org/issue-1/minilsm/) if you have a lot of free time.

We will keep it basic and store the data in a hash map data structure. The data will be accessible from a single exposed
endpoint. We will be supporting these four HTTP methods:

- `GET` for retrieving data
- `POST` for inserting and updating data
- `DELETE` for removing data

The actual name of the endpoint will be the key for the data. What does this mean? If you call
`GET http://<host>:<port>/user/42` the key will be `user/42`. The same goes for
`GET http://<host>:<port>/countries/data.xml` and any other symbols that are allowed in a URL. This means that our
key-value-store's keys are just strings - but since they are hashed this does not make much of a performance difference.

The name of the project? Iowa, because US states make good project names. Did you know that the name
comes from the Native American tribe of the same name? Well now you
[know](https://publications.iowa.gov/135/1/profile/8-14.html).

## Let's Code

One of the best moments in a developer's life: starting a new project (as opposed to the worst: finishing a project). We
start by creating a new Rust project with the `cargo` command.

```rust
cargo new --bin iowa
```

As mentioned, we need the actix-web framework dependency. Additionally, we will be adding
[clap](https://github.com/clap-rs/clap) for parsing command line arguments and
[env_logger](https://docs.rs/env_logger/latest/env_logger/) for logging.

```toml
[dependencies]
actix-web = "4"
clap = { version = "4.0.29", features = ["derive"] }
env_logger = "0.10.0"
```

Run the command `cargo run` to build and run the project and let cargo install all the dependencies.

We have to mark our `main()` method with the `actix_web::main` macro and change the signature to use the actix-web
framework.

```rust
#[actix_web::main]
async fn main() -> std::io::Result<()> {
  //...
}
```

## Command Line Arguments

We want to give the user the ability to specify host IP address and port for the HTTP server. Include the clap Parser
and specify a struct which can hold the command line parameters. The code comments act as descriptions that are
displayed on the `--help` output - so let's not be too shy with comments.

```rust
use clap::Parser;
```

```rust
/// Simple HTTP-based key-value-store
#[derive(Parser, Debug)]
#[command(author, version, about, long_about = None)]
struct Args {
    /// Host of the web service
    #[arg(long, default_value_t = String::from("0.0.0.0"))]
    host: String,

    /// Port of the web service
    #[arg(long, default_value_t = 1984)]
    port: u16,
}
```

The `cargo run -- --help` command shows if it worked. For more information about `clap` consider its
[official documentation](https://docs.rs/clap/latest/clap/) or the
[examples](https://github.com/clap-rs/clap/tree/master/examples).

We add the following first line to the `main()` method to parse the command line arguments, so we can use them later.

```rust
let args = Args::parse();
```

## Logging And State

We need to enable logging to output log messages in a standardized way. Add the following line within the `main()`
method after the command line argument parsing line from the step before.

```rust
env_logger::init_from_env(env_logger::Env::new().default_filter_or("info"));
```

Where do we store our data in memory? As mentioned before, we will be using a basic data structure for this: the
reliable hash map. And by the way: I am convinced every software developer should have implemented a hash map once to
learn about data structures and understand how they work. And then every good software developer should learn to use the
data structures provided by the program language's standard libraries. Never reinvent the wheel but understand how the
wheel works.

Add the `use` statements to the other ones and the `AppState` struct underneath.

```rust
use std::collections::HashMap;
use std::sync::Mutex;

// ...

/// App state which stores all keys and values.
struct AppState {
    store: Mutex<HashMap<String, String>>,
}
```

We are using keys of the `String` data type because we are storing the URL's endpoints as keys as described before.
The values are also stored as plain strings. The `Mutex` around our hash map is a must - the endpoints are methods
being called asynchronously and Rust does a pretty good job preventing race conditions. And that is helpful for our key-
value-store because we do not want one client to write a key while another one deletes it at the same time.

Within the `main()` method this app state needs to be instantiated so we can pass it to the HTTP server. This makes the
app state accessible from our endpoint implementations to read and write keys, as well as delete them (those poor
keys!).

```rust
let state = web::Data::new(AppState {
    store: Mutex::new(HashMap::new()),
});
```

## HTTP Server And Endpoints

To start the HTTP server we will add the following call at the end of the `main()` method to instantiate and run it. We
will:

- pass our app state that we instantiated before as argument,
- expose the endpoint handlers `get`, `set` and `del` to handle key reads, writes and deletes,
- wrap it with our logger,
- bind it to hostname and port from the command line arguments (or default values),
- and start it asynchronously.

```rust
HttpServer::new(move || {
        App::new()
            .app_data(state.clone())
            .service(get)
            .service(set)
            .service(del)
            .wrap(Logger::new("%a %{User-Agent}i"))
    })
    .bind((args.host, args.port))?
    .run()
    .await
```

Retrieving a key is handled by the `get()` method. The actix-web macro on top tells the handler which HTTP method is
used and what path is to be unwrapped. The key will be extracted from the request URI. This key is then used to look it
up in the hash map of the app state. We acquire a lock to appease the mutex and retrieve an `Option<>` return value from
calling the hash map's `get()` method. Depending on the result, we return the according key's value. Or - if no key was
found - the according "tough luck!" error message wrapped in a "HTTP 404 Not Found" gift for the client.

```rust
/// Returns a value from the given path.
#[get("/{key:.*}")]
async fn get(request: HttpRequest, data: web::Data<AppState>) -> HttpResponse {
    let key: String = request.uri().to_string();

    match data.store.lock().unwrap().get(&key) {
        Some(value) => HttpResponse::Ok()
            .content_type(ContentType::plaintext())
            .body(value.to_string()),
        _ => HttpResponse::NotFound()
            .content_type(ContentType::plaintext())
            .body("key not found"),
    }
}
```

The other two handlers are very similar. The `set()` method takes in the submitted data from a POST request as a
`web::Bytes` struct. These bytes get inserted into the hash map which will fit as many bytes as memory is available on
our machine (danger zone!). The method will either create a new entry in the hash map or overwrite an existing key if
existing.

```rust
/// Sets a value to the given path.
#[post("/{key:.*}")]
async fn set(request: HttpRequest, post: web::Bytes, data: web::Data<AppState>) -> HttpResponse {
    let key: String = request.uri().to_string();
    let value = String::from_utf8(post.to_vec()).unwrap();

    match data.store.lock().unwrap().insert(key, value) {
        None => HttpResponse::Created()
            .content_type(ContentType::plaintext())
            .body("new value inserted"),
        Some(_) => HttpResponse::Accepted()
            .content_type(ContentType::plaintext())
            .body("value updated"),
    }
}python
```

In almost the same manner: the deletion method. It removes the key if found. If the key does not exist, it returns the
same error message and HTTP 404 like the setter method.

```rust
/// Removes a given key.
#[delete("/{key:.*}")]
async fn del(request: HttpRequest, data: web::Data<AppState>) -> HttpResponse {
    let key: String = request.uri().to_string();

    match data.store.lock().unwrap().remove(&key) {
        Some(_) => HttpResponse::Ok()
            .content_type(ContentType::plaintext())
            .body("key and value removed"),
        _ => HttpResponse::NotFound()
            .content_type(ContentType::plaintext())
            .body("key not found"),
    }
}
```

## Running

It is time to run and test the key-value-store. Starting is easy by calling the cargo run command (by default, it will
bind to the localhost via 0.0.0.0 and to port 1984):

```sh
cargo run
```

Testing the API will be easy with the `curl` tool. Setting keys works via POST and submitting data:

```sh
curl -d'{ "name": "Chris" }' -X POST 'localhost:1984/user/123'
> new value inserted
```

In this case, `user/123` is our key. The value is a tiny JSON: `{ "name": "Chris" }`. We retrieve the same value by
calling the following command:

```sh
curl 'localhost:1984/user/123'
> { "name": "Chris" }
```

For deletion of this entry issue the same command but with the DELETE method and the key can no longer be retrieved.

```sh
curl -X DELETE 'localhost:1984/user/123'
> key and value removed
```

```sh
curl 'localhost:1984/user/123'
> key not found
```

Time to check in the code and make some evening tea.

## Bonus

The next steps left to the reader involve implementing more functionality. The following points are for inspiration and
ideas:

- **Containerization**:<br/>
  Packing the application into a Docker image
- **TLS support**:<br/>
  Because the world is a safer place with HTTPS
- **Authentication**:<br/>
  To not let anybody set and delete keys
- **Content-type support**:<br/>
  To store the appropriate type along the keys
- **PATCH for updating values**:<br/>
  Separating creating and updating views
- **Seeding data**:<br/>
  To not start the server completely empty
- **Memory usage**:<br/>
  Bringing in an upper limit for storage

For more complicated features, the following topics help out if you have too much free time at hand:

- **Persistence**:<br/>
  Storing the data and retrieving it when restarting is a nice thing to have if ephemeral storage gives you nightmares.
  Start looking at the options given at the beginning of the article.

- **Distribution**:<br/>
  Having a cluster of key-value-stores enables you to distribute the hash map app state over several machines and their
  memory. Start by looking at existing distribution protocols and how data can be partitioned on a cluster.

And as always: keep on coding and keep on creating!
