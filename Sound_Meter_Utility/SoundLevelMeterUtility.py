import os
import datetime
import csv
import xmlrpclib

class ClientUtility:
    def __init__(self, server_ip = None):
        self._server_ip = server_ip
        self._server = None
        self._server_exists = False

    def set_server_ip(self, server_ip):
        self._server_ip = server_ip

    def create_server(self):
        if self._server_ip != None:
            try:
                self._server = xmlrpclib.Server(self._server_ip)
                self._server_exists = True
            except:
                self._server_exists = False
                print "\nServer not found\n"
        else:
            self._server_exists = False
            print "\nServer not found\n"

    def upload_data(self, data_location, server_data_folder):
        data_name = os.path.split(data_location)[-1]
        if self.return_server_exists() == True:
            with open(data_location, "rb") as data_file:
                binary_data = xmlrpclib.Binary(data_file.read())
                self._server.push_data(binary_data,\
                    server_data_folder, data_name)

    def return_server_ip(self):
        return self._server_ip

    def return_server_exists(self):
        return self._server_exists

class SoundLevelMeterUtility:
    """
        This is a class utility for the Sound Level Meter.
    """
    def __init__(self,\
        raw_location = os.path.dirname(os.path.abspath(__file__)),\
        csv_location = os.path.dirname(os.path.abspath(__file__)),
        reshaped_location = os.path.dirname(os.path.abspath(__file__)),
        datetime_format = "%Y-%m-%d %H:%M:%S.%f",\
        local = True,\
        remove_csv = False, remove_reshaped = False,\
        frequency = 1, seconds_before_run = 1440):
        """
            Initialize the class.
        """
        self._ARCHIVEFILE = "archive.csv"
        self._raw_location = raw_location
        self._csv_location = csv_location
        self._reshaped_location = reshaped_location
        self._output_filename = "output.csv"
        self._datetime_format = datetime_format
        self._FREQUENCY = float(frequency)
        self._remove_csv = remove_csv
        self._remove_reshaped = remove_reshaped
        self._last_datetime_stamp = None
        self._seconds_before_run = seconds_before_run
        self._local = local

    def __add_output_file_location(self, filename):
        """
            This returns a path for a filename to the output file.
        """
        # Return a join of the filename and the output file path
        return os.path.join(self._output_file_location, filename)

    def project_extract(self):
        """
            This does a general project run by converting the raw files into
            csv's, then it reshaped the csv to a specified format.
        """
        # Run the convert_csv method for all the raw files
        # Run the reshape_csv method for all the csv files
        # Clean the folders if specified
        self.__open_folder_files(self.convert_csv,\
            self._raw_location)
        self.__open_folder_files(self.reshape_csv,\
            self._csv_location)
        if self._remove_csv == True:
            self.__open_folder_files(self.remove_csv,\
                self._csv_location)
        if self._remove_reshaped == True:
            self.__open_folder_files(self.remove_reshaped,\
                self._reshaped_location)

    def project_upload(self):
        """
            This uploads the project output to the server.
        """
        pass

    def convert_csv(self, raw_file_name):
        """
            This converts the raw file to a csv if it is not in the archive.
        """
        # Check the archive for the raw_file_name
        # Convert the raw file if it is not in the archive file
        self.__extract_non_archive(self.__convert_csv,\
            raw_file_name)

    def reshape_csv(self, csv_file_name):
        """
            This reshapes the csv file to a specific format if it is not in the
            archive.
        """
        # Check the archive for the csv_file_name
        # Reformat the csv
        self.__extract_non_archive(self.__reshape_csv,\
            csv_file_name)

    def __check_csv_run(self, raw_file_location):
        """
            This checks whether the raw file should be converted into a csv.
            The time of conversion is determined by the seconds_before_run.
            This checks whether enough time has passed before trying to convert
            the raw file.
            This is a precaution check since raw files that may still be open
            by the recording software.
        """
        # Open the raw file
        # Skip the header
        # Check last datetime added to the raw file
        # Return whether enough time has elapsed
        with open(raw_file_location, "r") as raw_file:
            raw_reader = csv.reader(raw_file, delimiter = ",")
            raw_row = raw_reader.next()
            while self.__check_header(raw_row) == True:
                raw_row = raw_reader.next()
            del raw_row
            for raw_row in raw_reader:
                    datetime_stamp = str(raw_row[0]) + " " + str(raw_row[1])
                    self._last_datetime_stamp =\
                        self.__convert_datetime_format(datetime_stamp)
        return self.__check_to_run()

    def __convert_csv(self, raw_file_name):
        """
            This converts the raw file to a csv.
            This is specific for the Sound Level Meter.
        """
        # Get the raw_file_location
        # Check if the run is allowed (enough time has elapsed)
        # If the run is allowed,
        #   Open the raw file
        #   Get the output csv location
        #   Write the raw file contents to a specified csv format
        #   (This format makes it easier to reshape for those not familiar with
        #   sql databasing)
        #   (datetime, sensor, value)
        print "\nCreating CSV\n"
        raw_file_location = os.path.join(self._raw_location, raw_file_name)
        print "Input: ", raw_file_location
        run = self.__check_csv_run(raw_file_location)
        if run == True:
            with open(raw_file_location, "r") as raw_file:
                raw_reader = csv.reader(raw_file, delimiter = ",")
                csv_file_location = os.path.join(self._csv_location,\
                    str(raw_file_name).replace(".txt", ".csv").\
                    replace(" ", "_"))
                with open(csv_file_location, "wb") as csv_file:
                    csv_writer = csv.writer(csv_file, delimiter = ",")
                    raw_row = raw_reader.next()
                    while self.__check_header(raw_row) == True:
                        raw_row = raw_reader.next()
                    del raw_row
                    for raw_row in raw_reader:
                        datetime_stamp = str(raw_row[0]) + " " +\
                            str(raw_row[1])
                        datetime_stamp = str(self.__convert_datetime_format(\
                            datetime_stamp))
                        csv_row = [datetime_stamp,\
                            str(raw_row[2])]
                        csv_writer.writerow(csv_row)

    def __check_reshape_run(self, csv_file_location):
        """
            This checks whether the csv file should be reformated.
            The time of conversion is determined by the seconds_before_run.
            This checks whether enough time has passed before trying to
            reshape the csv.
            This is a precaution check since csv files that may still be open
            by the recording software.
        """
        # Open the raw file
        # Skip the header
        # Check last datetime added to the raw file
        # Return whether enough time has elapsed
        with open(csv_file_location, "r") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter = ",")
            for csv_row in csv_reader:
                    datetime_stamp = csv_row[0]
                    self._last_datetime_stamp = datetime.datetime.strptime(\
                    datetime_stamp, "%Y-%m-%d %H:%M:%S")
        return self.__check_to_run()

    def __reshape_csv(self, csv_file_name):
        """
            This converts the raw file to a csv.
            This is specific for the Sound Level Meter.
            (The frequency is added since the raw data only outputs the time
            up to whole seconds).
        """
        # Get the csv file location
        # Check if the run is allowed
        # If allowed,
        # Write the csv into a reformated shape
        # (additionally, add the frequency to the time,
        # this will allow the data to be inserted into the database)
        print "\nReshaping CSV\n"
        csv_file_location = os.path.join(self._csv_location, csv_file_name)
        print "Input: ", csv_file_location
        run = self.__check_reshape_run(csv_file_location)
        if run == True:
            with open(csv_file_location, "r") as csv_file:
                csv_reader = csv.reader(csv_file, delimiter = ",")
                reshaped_file_location = os.path.join(self._reshaped_location,\
                    csv_file_name)

                # Pre-extract
                # Eject the first sets of data that doesn't match the normal
                # frequency. After this process, the script will process and
                # reshape the data as normal.
                precount = 0
                while 1:
                    # Pull the next set of data.
                    current_row = csv_reader.next()

                    # Extract the date time stamp.
                    current_date = current_row[0]

                    # Initial coditions
                    if precount == 0:
                        precount += 1

                        # Save a copy of the current date to next cycle.
                        last_date = current_date
                    else:
                        # Processing the same time set.
                        if current_date == last_date:
                            precount += 1

                        # Time set changes to the next set.
                        else:
                            # Exit out of the pre-extract sequence if the
                            # current set matches the required sample size.
                            # Note: The frequency is decreased by one because
                            # the recording software we are using only produces
                            # nine points for a dt of 0.1.
                            if precount == self._FREQUENCY - 1:
                                break
                            # The current set did not have the required amount
                            # of sample points, so the pre-extract will continue
                            # to gauge the next set of data points.
                            else:
                                precount = 1

                                # Save a copy of the current date to next cycle.
                                last_date = current_date

                # Extract
                with open(reshaped_file_location, "wb") as new_csv_file:
                    new_csv_writer = csv.writer(new_csv_file, delimiter = ",")

                    # Extract the date time stamp.
                    datetime_stamp = current_row[0]

                    # Initial extraction.
                    datetime_stamp = datetime_stamp + ".1"
                    sensor_id = "SDB7"
                    new_csv_row = [datetime_stamp, sensor_id, current_row[1]]
                    new_csv_writer.writerow(new_csv_row)
                    count = 1
                    last_date = current_row[0]
                    for csv_row in csv_reader:
                        # Check for set changing bountary.
                        if csv_row[0] == last_date:

                            # Keep track of how many sample points are present.
                            count += 1

                            # If there are more sample points then expected,
                            # then script will ignore them and continue.
                            if count > self._FREQUENCY - 1:
                                pass

                            # Otherwise, write the sample point with the time
                            # adjustment into the output file.
                            else:
                                datetime_stamp = csv_row[0]
                                datetime_stamp = datetime_stamp + '.' + str(count)
                                sensor_id = "SDB7"
                                new_csv_row = [datetime_stamp, sensor_id, csv_row[1]]
                                new_csv_writer.writerow(new_csv_row)
                        # Set bountary changed, reinitial count and write this
                        # this first sample point into the output file.
                        else:
                            count = 1
                            datetime_stamp = csv_row[0]
                            datetime_stamp = datetime_stamp + '.' + str(count)
                            sensor_id = "SDB7"
                            new_csv_row = [datetime_stamp, sensor_id, csv_row[1]]
                            new_csv_writer.writerow(new_csv_row)

                        # Save a copy of the current date to next cycle.
                        last_date = csv_row[0]

    def __extract_non_archive(self, function, file_name):
        """
            This checks if the filename is in the archive.
        """
        # Check if the file_name is in the archive
        # Make sure that the file is not a script
        # If it is not in the archive,
        # Add it to the archive and run the function on the file_name
        if ".py" not in file_name:
            in_archive = self.__check_in_archive(file_name)
            if in_archive == False:
                print file_name + " not in archive"
                function(file_name)
                self.__add_to_archive(file_name)
            else:
                print file_name + " in archive"

    def __set_datetime_stamp(self, datetime_stamp):
        """
            This sets the last_datetime_stamp checked.
        """
        # Set the last_datetime_stamp to the datetime_stamp
        self._last_datetime_stamp = self.__convert_datetime_format(\
	    datetime_stamp)

    def return_last_datetime_stamp(self):
        """
            This returns the last_datetime_stamp.
        """
        # Return the
        return self._last_datetime_stamp

    def __check_to_run(self):
        """
            This checks whether enough time has elapsed after the raw_file is
            finished.
        """
        # Get the current datetime
        # Check the time difference between the raw datetime and the current
        # datetime
        # Return True if enough time has elapsed
        # Else, return False
        datetime_today = datetime.datetime.now()
        time_difference = datetime_today - self._last_datetime_stamp
        if time_difference >= datetime.timedelta(\
            seconds = self._seconds_before_run):
            return True
        return False

    def __open_folder_files(self, function, folder_location):
        """
            This applies the function to all the files in the folder_location.
        """
        # Get the path of the folder_files
        # Run the function on the folder_files
        folder_files = os.listdir(folder_location)
        for folder_file in folder_files:
            function(folder_file)

    def __convert_datetime_format(self, datetime_stamp):
        """
            This converts a datetime_stamp string to the datetime format
            specified by the user.
        """
        # Strip the time of datetime_stamp
        return datetime.datetime.strptime(datetime_stamp,\
            self._datetime_format)

    def __check_in_archive(self, file_name):
        """
            This checks the archive for the file_name.
        """
        # Open the archive_file
        # Check each row for the file_name
        check_row = [file_name]
        with open(self._ARCHIVEFILE, "r") as archive_file:
            archive_reader = csv.reader(archive_file, delimiter = ",")
            for archive_row in archive_reader:
                if check_row == archive_row:
                    return True
        return False

    def __add_to_archive(self, file_name):
        """
            This adds the file_name to the archive.
        """
        # Open the archive
        # First check that the file_name is not in the archive
        # Add the file_name to the end of the archive
        in_archive = self.__check_in_archive(file_name)
        if in_archive == False:
            with open(self._ARCHIVEFILE, "a") as archive_file:
                archive_writer = csv.writer(archive_file, delimiter = ",")
                archive_row = [file_name]
                archive_writer.writerow(archive_row)

    def clear_archive(self):
        """
            This clears the archive.
        """
        # Open the archive file as write
        with open(self._ARCHIVEFILE, "wb"):
            pass
            print "Cleared " + self._ARCHIVEFILE

    def __check_header(self, data_row):
        """
            This checks for a header in the row given.
        """
        # Return True if the row is a header
        if len(data_row) < 3:
            return True
        else:
            return False

    def remove_csv(self, csv_file_name):
        """
            This removes the csv.
        """
        # Remove the csv if it exists
        try:
            if ".py" not in csv_file_name:
                csv_file_location = os.path.join(self._csv_location, csv_file_name)
                os.remove(csv_file_location)
        except:
            pass

    def remove_reshaped(self, reshaped_file_name):
        """
            This removes the reshapes.
        """
        # Remove the reshape if it exists.
        try:
            if ".py" not in reshaped_file_name:
                reshaped_file_location = os.path.join(self._reshaped_location,\
                    reshaped_file_name)
                os.remove(reshaped_file_location)
        except:
            pass
