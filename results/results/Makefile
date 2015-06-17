# vim: wrap
#
BUILDDIR := build
CONFIGS := sift-kmeans-1000-02-slic-lsi-segments sift-kmeans-1000-02-canny-lsi-segments sift-kmeans-1000-02-otsu-lsi-segments sift-kmeans-1000-02-slic-tfidf-segments sift-kmeans-1000-02-canny-tfidf-segments sift-kmeans-1000-02-otsu-tfidf-segments sift-som-1000-02-slic-lsi-segments surf-kmeans-1000-02-slic-lsi-segments surf-kmeans-1000-02-canny-lsi-segments surf-kmeans-1000-02-otsu-lsi-segments surf-kmeans-1000-02-slic-tfidf-segments surf-kmeans-1000-02-canny-tfidf-segments surf-kmeans-1000-02-otsu-tfidf-segments surf-som-1000-02-slic-lsi-segments sift-kmeans-2000-02-slic-lsi-segments sift-kmeans-2000-02-canny-lsi-segments sift-kmeans-2000-02-otsu-lsi-segments sift-kmeans-2000-02-slic-tfidf-segments sift-kmeans-2000-02-canny-tfidf-segments sift-kmeans-2000-02-otsu-tfidf-segments sift-som-2000-02-slic-lsi-segments surf-kmeans-2000-02-slic-lsi-segments surf-kmeans-2000-02-canny-lsi-segments surf-kmeans-2000-02-otsu-lsi-segments surf-kmeans-2000-02-slic-tfidf-segments surf-kmeans-2000-02-canny-tfidf-segments surf-kmeans-2000-02-otsu-tfidf-segments surf-som-2000-02-slic-lsi-segments sift-kmeans-2000-0-none-bow-images surf-kmeans-2000-0-none-bow-images sift-kmeans-4000-0-none-bow-images surf-kmeans-4000-0-none-bow-images
DATS := precision recall fscore
DATS_TRANSPOSE := precisiontranspose recalltranspose fscoretranspose
DATS_AVG := fscoreavg
DATS_DATASET := dataset
DATS_RETRIEVAL := retrieval
TEX := ukbench-imagesamples mirflickr-imagesamples ukbench-results1 ukbench-results2 mirflickr-results1 mirflickr-results2

UKBENCH_DIR := $(BUILDDIR)/ukbench
MIRFLICKR_DIR := $(BUILDDIR)/mirflickr

UKBENCH_CONFIGS := $(CONFIGS:%=$(UKBENCH_DIR)/%.results)
MIRFLICKR_CONFIGS := $(CONFIGS:%=$(MIRFLICKR_DIR)/%.results)

UKBENCH_PDF := $(DATS:%=$(UKBENCH_DIR)-%.pdf)
MIRFLICKR_PDF := $(DATS:%=$(MIRFLICKR_DIR)-%.pdf)

UKBENCH_TRANSPOSE_PDF := $(DATS_TRANSPOSE:%=$(UKBENCH_DIR)-%.pdf)
MIRFLICKR_TRANSPOSE_PDF := $(DATS_TRANSPOSE:%=$(MIRFLICKR_DIR)-%.pdf)

UKBENCH_AVG_PDF := $(DATS_AVG:%=$(UKBENCH_DIR)-%.pdf)
MIRFLICKR_AVG_PDF := $(DATS_AVG:%=$(MIRFLICKR_DIR)-%.pdf)

UKBENCH_RETRIEVAL_PDF := $(DATS_RETRIEVAL:%=$(UKBENCH_DIR)-%.pdf)
MIRFLICKR_RETRIEVAL_PDF := $(DATS_RETRIEVAL:%=$(MIRFLICKR_DIR)-%.pdf)

# UKBENCH_DATASET_PDF := $(DATS_DATASET:%=$(MIRFLICKR_DIR)-%.pdf)

MIRFLICKR_DATASET_PDF := $(DATS_DATASET:%=$(MIRFLICKR_DIR)-%.pdf)
ALL_TEX := $(TEX:%=$(BUILDDIR)/%.tex)

tex: $(ALL_TEX)

$(ALL_TEX):
	python2 generate-dat.py $@ > $@

graphs: $(UKBENCH_PDF) $(MIRFLICKR_PDF) $(UKBENCH_TRANSPOSE_PDF) $(MIRFLICKR_TRANSPOSE_PDF) $(UKBENCH_AVG_PDF) $(MIRFLICKR_AVG_PDF) $(UKBENCH_RETRIEVAL_PDF) $(MIRFLICKR_RETRIEVAL_PDF) $(MIRFLICKR_DATASET_PDF)

$(MIRFLICKR_PDF) $(UKBENCH_PDF):
	python2 generate-dat.py $(subst .pdf,.dat,$@) > $(subst .pdf,.dat,$@)
	gnuplot -e "infile='$(subst .pdf,.dat,$@)'; outfile='$(subst .pdf,.eps,$@)'; items=32" stackedbars.gnu
	epstopdf $(subst .pdf,.eps,$@)
	gnuplot -e "infile='$(subst .pdf,.dat,$@)'; outfile='$(subst .pdf,-points.eps,$@)'; items=32" points.gnu
	epstopdf $(subst .pdf,-points.eps,$@)
	python2 average.py < $(subst .pdf,.dat,$@) > $(subst .pdf,-avg.dat,$@)
	gnuplot -e "infile='$(subst .pdf,-avg.dat,$@)'; outfile='$(subst .pdf,-avg.eps,$@)'" histogram.gnu
	epstopdf $(subst .pdf,-avg.eps,$@)

$(MIRFLICKR_TRANSPOSE_PDF) $(UKBENCH_TRANSPOSE_PDF):
	python2 generate-dat.py $(subst .pdf,.dat,$@) > $(subst .pdf,.dat,$@)
	gnuplot -e "infile='$(subst .pdf,.dat,$@)'; outfile='$(subst .pdf,.eps,$@)'; items=50" stackedbars.gnu
	epstopdf $(subst .pdf,.eps,$@)
	gnuplot -e "infile='$(subst .pdf,.dat,$@)'; outfile='$(subst .pdf,-points.eps,$@)'; items=50" points.gnu
	epstopdf $(subst .pdf,-points.eps,$@)
	python2 average.py < $(subst .pdf,.dat,$@) > $(subst .pdf,-avg.dat,$@)
	gnuplot -e "infile='$(subst .pdf,-avg.dat,$@)'; outfile='$(subst .pdf,-avg.eps,$@)'" histogram.gnu
	epstopdf $(subst .pdf,-avg.eps,$@)

$(MIRFLICKR_AVG_PDF) $(UKBENCH_AVG_PDF):
	python2 generate-dat.py $(subst .pdf,.dat,$@) > $(subst .pdf,.dat,$@)
	gnuplot -e "infile='$(subst .pdf,.dat,$@)'; outfile='$(subst .pdf,.eps,$@)'" histogram.gnu
	epstopdf $(subst .pdf,.eps,$@)

$(MIRFLICKR_DATASET_PDF):
	python2 generate-tags.py $(subst .pdf,.dat,$@) > $(subst .pdf,.dat,$@)
	gnuplot -e "infile='$(subst .pdf,.dat,$@)'; outfile='$(subst .pdf,.eps,$@)'" dataset.gnu
	epstopdf $(subst .pdf,.eps,$@)

$(MIRFLICKR_RETRIEVAL_PDF) $(UKBENCH_RETRIEVAL_PDF):
	python2 generate-dat.py $(subst .pdf,.dat,$@) > $(subst .pdf,.dat,$@)
	python2 average.py < $(subst .pdf,.dat,$@) > $(subst .pdf,-avg.dat,$@)
	gnuplot -e "infile='$(subst .pdf,-avg.dat,$@)'; outfile='$(subst .pdf,-avg.eps,$@)'" histogram.gnu
	epstopdf $(subst .pdf,-avg.eps,$@)
	gnuplot -e "infile='$(subst .pdf,.dat,$@)'; outfile='$(subst .pdf,.eps,$@)'; items=32" points.gnu
	epstopdf $(subst .pdf,.eps,$@)


results: $(UKBENCH_CONFIGS) $(MIRFLICKR_CONFIGS)

$(UKBENCH_DIR):
	mkdir -p $(UKBENCH_DIR)

$(UKBENCH_DIR)/%: $(UKBENCH_DIR)
	python2 execute-configuration.py ../datasets/ukbench-training $@ > $@

$(MIRFLICKR_DIR):
	mkdir -p $(MIRFLICKR_DIR)

$(MIRFLICKR_DIR)/%: $(MIRFLICKR_DIR)
	python2 execute-configuration.py ../datasets/mirflickr-training $@ > $@

clean:
	rm -rf $(BUILDDIR)

