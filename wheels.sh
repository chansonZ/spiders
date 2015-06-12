#!/bin/bash

# Cron job for the 'wheels' scraping project.
# Author: loic@cyberpunk.bike

# Define the working environment
scraper_exe='/home/loic/code/wheels/venv/bin/scrapy'
working_dir='/home/loic/code/wheels/crawler'
output_file='/home/loic/code/wheels/output/wheels.csv'

# Specify the spiders (one spider per retailer)
declare -a spiders=("bike-components")

cd ${working_dir}

for spider in "${spiders[@]}"
	do
		echo ${spider}
		# Scraping results are appended to the output file.
		eval "${scraper_exe} crawl --output=${output_file} --output-format=csv ${spider} "	
	done

