import sys
import os
import subprocess
import shutil
import logging

import todo_enums as enums
import convertMKV
import zip_files

##############################
# Logging
##############################
logger = logging.getLogger('media_work_queue')
logger.setLevel(logging.DEBUG)

# Formatter
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s:%(message)s')

# File Handler
file_handler = logging.FileHandler('media_work_queue_logs.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

# Console Handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)


##############################
# Enums
##############################
VideoType = enums.VideoType


##############################
# Helpers
##############################

TV = VideoType.tv
MOVIE = VideoType.movie

failures = ''

def convert_and_zip(type, name, path):
	try:
		description = 'convert {} and zip'.format(name)
		logger.info('Starting: {}'.format(description))
		convert(type, name, path)
		zip(name, path)
		logger.info('Finished: {}'.format(description))
	except Exception as e:
		logger.error('Failed to {}. Failed with Error: {}'.format(description, e))

def unzip_and_convert(type, name, path):
	try:
		description = 'unzip {} and convert'.format(name)
		logger.info('Starting: {}'.format(description))
		unzip(name, path)
		convert(type, name, path)
		logger.info('Finished: {}'.format(description))
	except Exception as e:
		logger.error('Failed to {}. Failed with Error: {}'.format(description, e))

def convert(type, name, path):
	try:
		description = 'convert {}'.format(name)
		logger.info('Starting: {}'.format(description))
		convertMKV.convert(type, path)
		logger.info('Finished: {}'.format(description))
	except Exception as e:
		failures = failures + '\n' + description
		logger.error('Failed to {}. Failed with Error: {}'.format(description, e))

def zip(name, path):
	try:
		description = 'zip {}'.format(name)
		logger.info('Starting: {}'.format(description))
		zip_files.zip(path)
		logger.info('Finished: {}'.format(description))
	except Exception as e:
		failures = failures + '\n' + description
		logger.error('Failed to {}. Failed with Error: {}'.format(description, e))

def unzip(name, path):
	try:
		description = 'unzip {}'.format(name)
		logger.info('Starting: {}'.format(description))
		zip_files.unzip(path)
		logger.info('Finished: {}'.format(description))
	except Exception as e:
		failures = failures + '\n' + description
		logger.error('Failed to {}. Failed with Error: {}'.format(description, e))

def unzip_rar(type, name, path):
	try:
		description = 'unzipping rar {}'.format(name)
		logger.info('Starting: {}'.format(description))
		zip_files.unzip_rar(type, path)
		logger.info('Finished: {}'.format(description))
	except Exception as e:
		failures = failures + '\n' + description
		logger.error('Failed to {}. Failed with Error: {}'.format(description, e))

##############################
# Start Here
##############################

convert_and_zip(MOVIE, 'The Jungle Book', 'G:\Media\Movies\The Jungle Book')
convert_and_zip(MOVIE, 'The Legend of Tarzan', 'G:\Media\Movies\The Legend of Tarzan')
convert_and_zip(MOVIE, 'X-Men Apocalypse', 'G:\Media\Movies\X-Men Apocalypse')

convert_and_zip(TV, 'Downton Abbey', 'G:\Media\TV\Downton Abbey')
convert_and_zip(TV, 'Firefly', 'G:\Media\TV\Firefly')
convert_and_zip(TV, 'Moonlight', 'G:\Media\TV\Moonlight')
convert_and_zip(TV, 'Wonderfalls', 'G:\Media\TV\Wonderfalls')

name = "3rd Rock from the Sun"
path = 'G:\Media\TV\3rd Rock from the Sun'
convert(TV, name, path)

name = "Doctor Who"
path = 'G:\Media\TV\Doctor Who'
unzip_and_convert(TV, name, path)

name = 'Rar_unzip Farscape'
path = 'G:\Media\TV\Farscape\Farscape'
rar_unzip(TV, name, path)


##############################
# Log Failures
##############################
if failures == '':
	logger.info("Queue completed successfully.")
else:
	logger.info("Queue completed with errors: {}".format(failures))
