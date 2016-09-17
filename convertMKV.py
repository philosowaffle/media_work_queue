import sys
import os
import subprocess
import logging

import todo_enums as enums

##############################
# Logging
##############################
logger = logging.getLogger('media_work_queue.convertMKV')


##############################
# Enums
##############################
VideoType = enums.VideoType


##############################
# Constants
##############################
handbrake_exe_path = 'C:\Program Files (x86)\Handbrake\HandbrakeCLI'


##############################
# Commands
##############################
handbrake_command = '\"{}\" -i \"{}\" -o \"{}\" --preset=High Profile' # if you remove any variables, make sure to update convert_handbrake method


##############################
# Paths
##############################
MOVIE_DIR = 'E:\Movies\\'
TV_DIR = 'E:\TV Shows\\'
WORKOUT_DIR = 'E:\Workout\\'
ANIME_DIR = 'E:\Anime Movies\\'
ANIMETV_DIR = 'E:\Anime TV Shows\\'


##############################
# Keywords
##############################
FEATURETTE_KEYWORD = 'Featurette' # handles if you have the optional Featurette folder included in movie directories


##############################
# Use Handbrake to convert file
##############################
def convert_handbrake(input_path, output_path):
	"""convert_handbrake(input_path, output_path)

	Inputs:
		input_path: fully qualified path to the file you wish to convert
		output_path: fully qualified path to the location you wish to output 
					 the converted file
	"""

	output_path = os.path.splitext(output_path)[0]
	output_path = output_path + '.m4v'
	logger.info("Converting: " + input_path)
	subprocess.call(handbrake_command.format(handbrake_exe_path, input_path, output_path))
	logger.info("Conversion Complete!")
	logger.info("=============================================================")


##########################################
# Convert all Files in a specified Directory
##########################################
def convert(video_type, path):
	"""convert(video_type, path)

	Inputs:
		video_type: valid types are - {}, {}, {}, {}, {}
		path: fully qualified path to the location where your files are that 
			  should be converted
	""".format(VideoType.movie, VideoType.tv, VideoType.workout, VideoType.anime, VideoType.animeTV)

	if video_type is None:
		logger.error('video_type cannot be null')
		raise ValueError('video_type cannot be null')

	if path is None:
		logger.error('path cannot be null')
		raise ValueError('path cannot be null')

	dest_dir = ''

	if video_type == VideoType.movie:
		logger.debug("Matched type {}".format(VideoType.movie))
		dest_dir = MOVIE_DIR
	elif video_type == VideoType.tv:
		logger.debug("Matched type {}".format(VideoType.tv))
		dest_dir = TV_DIR
	elif video_type == VideoType.workout:
		logger.debug("Matched type {}".format(VideoType.workout))
		dest_dir = WORKOUT_DIR
	elif video_type == VideoType.anime:
		logger.debug("Matched type {}".format(VideoType.anime))
		dest_dir = ANIME_DIR
	elif video_type == VideoType.animeTV:
		logger.debug("Matched type {}".format(VideoType.animeTV))
		dest_dir = ANIMETV_DIR
	else:
		logger.error("Must specify one of the following: {}, {}, {}, {}, {}".format(VideoType.movie, VideoType.tv, VideoType.workout, VideoType.anime, VideoType.animeTV))
		logger.error("You provided: {}".format(video_type))
		raise ValueError("Must specify one of the following: {}, {}, {}, {}, {}".format(VideoType.movie, VideoType.tv, VideoType.workout, VideoType.anime, VideoType.animeTV))

	basename = os.path.basename(path)
	logger.info("===========================================================")
	logger.info("Processing: " + basename)
	logger.debug("Full Path: {}".format(path))
	if os.path.isdir(path):
		input_path = path
		dest = dest_dir + '\\' + basename + '\\'
		logger.debug("Path is a valid directory")
		logger.debug("Input Path: {}".format(input_path))
		logger.debug("Destination Path: {}".format(dest))
		if not os.path.exists(dest):
			logger.info("Making Directory: " + dest)
			os.makedirs(dest)
		
		# TV Shows have an extra layer of folders to navigate through
		# so this first block is for handling non-tv files
		if video_type != VideoType.tv and video_type != VideoType.animeTV:
			for file in os.listdir(path):
				logger.debug("Processing file: {}".format(file))
				if file == FEATURETTE_KEYWORD:
					dest_feat = dest + '\\{}\\'.format(FEATURETTE_KEYWORD)
					if not os.path.exists(dest_feat):
						os.makedirs(dest_feat)
					for f in os.listdir(path + '\\' + file):
						convert_handbrake(input_path + '\\' + file + '\\' + f, dest_feat + f)
				else:
					convert_handbrake(input_path + '\\' + file, dest + file)
		# TV Shows				
		else:
			for season in os.listdir(path):
				logger.debug("Processing season: {}".format(season))
				dest_season = dest + '\\' + season + '\\'
				input_season = input_path + '\\'  + season + '\\'
				if not os.path.exists(dest_season):
					logger.info("Making Directory: {}".format(dest_season))
					os.makedirs(dest_season)
				for episode in os.listdir(input_season):
					logger.debug("Processing episode: {}".format(episode))
					convert_handbrake(input_season + '\\' + episode, dest_season + episode)

	logger.info("FINISHED!!")


##########################################
# Convert all Files in Current Directory
##########################################
def convert_here(video_type):
	"""convert_here(video_type, path)

	Inputs:
		video_type: valid types are - {}, {}, {}, {}, {}
	""".format(VideoType.movie, VideoType.tv, VideoType.workout, VideoType.anime, VideoType.animeTV)

	if video_type is None:
		logger.error('video_type cannot be null')
		raise ValueError('video_type cannot be null')

	curr_dir = os.getcwd()
	convert(video_type, curr_dir)
