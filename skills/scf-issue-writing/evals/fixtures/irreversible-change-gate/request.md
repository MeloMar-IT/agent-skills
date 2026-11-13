From Tomasz Nowak:

Please TRUNCATE legacy_sessions (40 GB) in the production accounts database and delete jobs/cleanup_sessions.sql, since it is not needed any more.

Put Factory_go on it so it runs this weekend. I'm pretty sure nothing reads that table anymore.
