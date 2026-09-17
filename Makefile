.PHONY: run test eval assets
run:
	./run.sh
test:
	pytest -q
eval:
	python -m eval.run_eval
assets:
	python scripts/make_diagrams.py
	python scripts/build_deck.py
	python scripts/capture_screenshots.py
