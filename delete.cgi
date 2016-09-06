#!/usr/bin/perl -T

use strict;
use warnings;
use CGI;
use CGI::Carp qw/fatalsToBrowser/;
use File::Basename;

my $query = new CGI;

my $dir = '../photos';	# relative location of file directory from this cgi

# a list of valid characters that can be in filenames
my $filename_characters = 'a-zA-Z0-9_.-';

my $file = $query->param('filename');
my $sure = $query->param('sure');

# get the filename and the file extension
# this could be used to filter out unwanted filetypes
# see the File::Basename documentation for details
my ($filename,undef,$ext) = fileparse($file,qr{\..*});

# convert spaces to underscores "_"
$filename =~ tr/ /_/;

# remove illegal characters
$filename =~ s/[^$filename_characters]//g;

# append extension to filename
$filename .= $ext;

print $query->header ( );

# satisfy taint checking
if ($filename =~ /^([$filename_characters]+)$/) {
   $filename = $1;
}
else{
	&notify_box("The filename is not valid","Filenames can only contain these characters: $filename_characters");
	exit(0);
} 

if ($filename eq '')	{	# verify filename is not null
	&notify_box("No file selected","No file was selected. Please <b>select a file</b> before clicking DELETE.");
} else	{
	&sure_or_not;
}

sub sure_or_not {		# verify user confirmed delete, and then delete
	if ($sure eq "yes") {
		unlink("$dir/$filename") or die "Can't delete $dir/$filename\n$!\n";	# delete the file
		unlink("$dir/thumbs/$filename") or die "Can't delete $dir/thumbs/$filename\n$!\n";	# delete the file
		&notify_box("File Deleted","File <b>$filename</b> has been permanently deleted.");
	}	else {
		&notify_box("File NOT Deleted","File <b>$filename</b> was <b>NOT</b> deleted. Verify that you selected the radio button marked <b>YES I am sure</b>.");
	}
}

sub notify_box {
my ($legend_text, $notify_text) = @_;
print <<"EOFEOF";
<!DOCTYPE HTML>
<html>
	<head>
		<title>File Manager</title>
		<link rel="stylesheet" type="text/css" href="styles.css" /><!-- graydata.com -->
	</head>
	<body>
		<fieldset>
			<fieldset><legend>$legend_text</legend>
				<br />
				$notify_text
				<br /><br />
				Go back to the <a href="index.cgi">File Manager</a> page.
			</fieldset>
		</fieldset>
	</body>
</html>
EOFEOF
}
