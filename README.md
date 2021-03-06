smstotwitter
============

Sms to twitter is a small python script designed to forward sms messages from
an sms to web gateway (such as bulksms.co.uk) to twitter.

Keywords specified in the configuarion file are added to each message if they
are not already present. Messages are truncated to ensure keywords fit.

Input is via http post to /incomingsms. Configuration is via a yaml
configuration file (see sample_config.yml).

Sms to twitter can be run as a standalone flask application or within another
webserver via wsgi (see smstotwitter.wsgi).

![smstotwitter diagram](https://raw.github.com/hughsaunders/smstotwitter/master/smstotwitter.png)

#### Sample apache vhost for using WSGI:

```apache
<VirtualHost *:80>
	ServerName example.com
	ServerAdmin admin@example.com

	WSGIDaemonProcess smstotwitter threads=5
	WSGIScriptAlias / /path/to/smstotwitter/smstotwitter.wsgi
	WSGIScriptReloading On
	SetEnv SMSTOTWITTER_CONFIG_FILE /path/to/smstotwitter/config.yml

	ErrorLog ${APACHE_LOG_DIR}/sms_error.log

	# Possible values include: debug, info, notice, warn, error, crit,
	# alert, emerg.
	LogLevel warn

	CustomLog ${APACHE_LOG_DIR}/sms_access.log combined
</VirtualHost>
```
