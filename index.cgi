#!/usr/bin/perl -T

use strict;
use warnings;
use CGI;
use CGI::Carp qw/fatalsToBrowser/;

my $query = new CGI;

my $dir = '../photos';	# relative location of file directory from this cgi

my @files = <$dir/*>;
my $list = '';

foreach (@files)	{		# build html form of existing filenames
	$_ =~ s!$dir/!!gi;		# remove path from filename
	if ($_ ne 'thumbs') {
		$list .= "<input name=\"filename\" id=\"filename\" type=\"radio\" value=\"$_\" /><a href=\"$dir/$_\"><img alt=\"$_\" src=\"$dir/thumbs/$_\" class=\"photos-images\" /></a> &nbsp &nbsp &nbsp &nbsp \n";
	}
}

if ($list eq '')	{	# what to print if there werent any files
	$list .= "<red>There were no files found in the $dir directory. After you have uploaded a file, it will appear in this list.</red>";
}

print $query->header ( );
print <<"EOFEOF";
<!DOCTYPE HTML>
<html>
	<head>
		<title>Photo Manager</title>
		<link rel="stylesheet" type="text/css" href="styles.css" />
	</head>
	<body>
		<fieldset>
			Thank you for using the photo manager.<br /><br />
			You can use the options below to upload a new photo, or to delete an existing photo.<br />
			Current working directory: $dir
		</fieldset>
		<br />
		<fieldset>
			<fieldset><legend>Upload Photos</legend>
				<form id="uploadFiles" action="upload.cgi" method="post" enctype="multipart/form-data">	<!-- begin uploadFiles form -->
					<input type="file" name="fileToUpload" />
					<input type="submit" name="Submit" value="Upload chosen file now" />
				</form>	<!-- end uploadFiles form -->
			</fieldset>
		</fieldset>
		<br />
		<fieldset>
			<fieldset><legend>Delete Photos</legend>
				Select the radio button to the left of the photo to be deleted. You can only delete one photo at a time.<br />
				<form id="deleteFiles" action="delete.cgi" method="post">	<!-- begin deleteFiles form -->
					$list<br />
					<fieldset><legend>Are you SURE?</legend>
						Are you really sure that you want to <b>PERMANENTLY DELETE</b> the selected photo and its thumbnail?<br />
						<input name="sure" id="sure" type="radio" value="yes"><b>YES</b> I am sure.<br />
						<input name="sure" id="sure" type="radio" value="no" checked="checked"><b>NO</b> I am not sure.
					</fieldset>
					<br />
					<input type="submit" name="Submit" value="Click this button to delete the selected photo now" />
				</form>	<!-- end deleteFiles form -->
			</fieldset>
		</fieldset>
	</body>
</html>
EOFEOF

