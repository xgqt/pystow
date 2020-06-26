BIN = pystow


.PHONY: all clean install uninstall distclean


all:
	@echo did nothing. try targets: install, or uninstall.


clean:
	$(RM) -dr $(BIN).egg-info
	$(RM) -dr build
	$(RM) -dr dist
	$(RM) -dr $(BIN)/__pycache__


install:
	python setup.py -v install --user


uninstall:
	pip uninstall -v -y $(BIN)


distclean: uninstall
distclean: clean
