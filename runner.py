import argparse
from modules.application import Application
from modules.enumerators import Constants

parser = argparse.ArgumentParser(description='Program will automatically maintain copy of the source folder tree into the destination folder, regularly according defined time interval.')
parser.add_argument('-src','--source_path', help='Specify source path')
parser.add_argument('-dst','--destination_path', help='Specify destination path')
parser.add_argument('-sync','--synchronization_interval', help='Specify synchorinzation iterval. By default in seconds.')
parser.add_argument('-logpath','--log_path', help='Specify log path, log file name\'ll be created automatically based on current date&time.')
arguments = vars(parser.parse_args())

if __name__ == '__main__':
    app = Application(arguments)
    if(app.STATUS!=Constants.EROOR):
        app.logger.info("You can interrupt the application execution anytime, by pressing letter 'q'.")
        app.run()
    else:
        app.logger.warning("Please, fix the input arguments and rerun the application again.")