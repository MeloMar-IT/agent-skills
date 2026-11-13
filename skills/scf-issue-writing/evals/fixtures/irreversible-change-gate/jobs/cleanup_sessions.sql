DELETE FROM legacy_sessions WHERE created_at < now() - interval '90 days';
