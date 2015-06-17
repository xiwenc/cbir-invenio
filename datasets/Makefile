all: clean create-ukbench create-mirflickr
clean: clean-mirflickr clean-ukbench

clean-ukbench:
	rm -rf ukbench-test
	rm -rf ukbench-training

clean-mirflickr:
	rm -rf mirflickr-test
	rm -rf mirflickr-training

create-ukbench:
	mkdir ukbench-test ukbench-training
	python ukbench.py ~/Documents/ukbench 200

create-mirflickr:
	mkdir mirflickr-test mirflickr-training
	python mirflickr.py ~/Documents/mirflickr 200
