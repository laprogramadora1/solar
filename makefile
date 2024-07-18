default: start

module:=index
app:=app

.PHONY: start
start:
	@ nohup ./virtual/bin/gunicorn -b "0.0.0.0:5000" \
	-w 4 --daemon ${module}:${app} --access-logfile /home/cis/elizabeth/solar/solar.log

.PHONY: status
status:
	ps -ef | grep -i gunicorn

.PHONY: stop
stop:
	@ for pid in \
	$$(ps -eo pid,command | grep "gunicorn.*${module}:${app}" \
	| grep -v grep | awk '{print $$1}'); do \
	kill -9 $${pid}; \
	done 
