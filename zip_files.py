import sys
import os
import subprocess
import shutil
import logging

import media_work_queue_enums as enums


##############################
# Logging
##############################
logger = logging.getLogger('media_work_queue.zip_files')


##############################
# Enums
##############################
VideoType = enums.VideoType


##############################
# Constants
##############################
archive_password = 'password'
zip_exe_path = 'C:\\Program Files\\7-Zip\\7z'


##############################
# Commands
##############################
zip_command = '\"{}\" a \"{}\" \"{}\" -p{}' # if you remove any variables, make sure to update zip method
unzip_command = '\"{}\" x \"{}\" -p{} -o\"{}\"' # if you remove any variables, make sure to update unzip method
unzip_rar = '\"{}\" x \"{}\" -o\"{}\"' # if you remove any variables, make sure to update unzip_rar method


##############################
# Zip directory
##############################
def zip(dir_path):
	"""zip(dir_path)

	Inputs:
		dir_path: fully qualified path to the directory to zip
	"""

	if dir_path is None:
		logger.error('path cannot be null')
		raise ValueError('path cannot be null')
	
	if os.path.isdir(dir_path):
		output = dir_path + '.7z'
		logger.info("==================================================")
		logger.info("Zipping: " + dir_path + " To: " + output)
		try:
			command = zip_command.format(zip_exe_path, output, dir_path, archive_password)
			logger.debug("Command: {}".format(command))
			subprocess.call(command)
			logger.info("Zip Complete!")
			logger.info("Deleteing " + dir_path)
			shutil.rmtree(dir_path)
			logger.info("==================================================")
		except:
			logger.error('Potential Error On: ' + dir_path)


####################################################
# Unzip all Archive Files in specified directory
####################################################
def unzip(dir_path):
	"""unzip(dir_path)

	Inputs:
		dir_path: fully qualified path to the location where your files are that 
			  should be unzipped
	"""

	if dir_path is None:
		logger.error('path cannot be null')
		raise ValueError('path cannot be null')

	for zipFile in os.listdir(dir_path):
		input = dir_path + '\\' + zipFile
		logger.info("==================================================")
		logger.info("Unzipping: " + input)
		logger.info("Destination: " + dir_path)
		try:
			command = unzip_command.format(zip_exe_path, input, archive_password, dir_path)
			logger.debug("Command: {}".format(command))
			subprocess.call(command)
			logger.info("Unzip Complete!")
			logger.info("==================================================")
		except:
			logger.error('Potential Error On: ' + input)


##############################
# Unzip Rar Files
##############################
def unzip_rar(video_type, dir_path):
	"""unzip(dir_path)

	Inputs:
		video_type: valid types are - {}
		dir_path: fully qualified path to the location where your files are that 
			  should be unzipped
	""".format(VideoType.tv)

	if video_type is None:
		logger.error('video_type cannot be null')
		raise ValueError('video_type cannot be null')

	if dir_path is None:
		logger.error('path cannot be null')
		raise ValueError('path cannot be null')

	if video_type == VideoType.tv:
		for season in os.listdir(dir_path):
			# Season 01, 02, ect.
			season_dir = dir_path + '\\' + season
			logger.debug("Processing season: {}".format(season_dir))
			# Rar files should be organized in directory per episode
			for episode in os.listdir(season_dir):
				episode_path = season_dir + '\\' + episode
				for f in os.listdir(episode_path):
					file_path = episode_path + '\\' + f
					filename, file_extension = os.path.splitext(file_path)
					if file_extension == '.rar':
						input = file_path
						logger.info("==================================================")
						logger.info("Unzipping: " + input)
						try:
							command = unzip_rar.format(zip_exe_path, input, season_dir)
							logger.debug("Command: {}".format(command))
							subprocess.call(command)
							logger.info("Unzip Complete!")
							logger.info("==================================================")
						except:
							logger.info('Potential Error On: ' + input)
