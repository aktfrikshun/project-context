# ChloKat Public Archive

Role: early Rails implementation of the public searchable archive, latest-news hub, release discovery, and superfan surface for `chlokat.frikshun.com`.

The private transformation engine lives in Creator OS. Both currently share a PostgreSQL database, and this Rails application is intended to own coordinated durable migrations for artifacts, releases, public posts, search, and fan-safe data.

Important source: `README.md`. The repository is still sparse; product intent is more established than feature completeness. Keep Rails and database implementation details local while promoting the public/private boundary and data-ownership rule.
