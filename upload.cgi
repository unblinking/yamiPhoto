#!/usr/bin/perl -T

use strict;
use warnings;
use CGI;
use CGI::Carp qw/fatalsToBrowser/;
use File::Basename;

# set the maximum limit for file uploads  
$CGI::POST_MAX = 1024 * 5000; #adjust as needed (1024 * 5000 = 5MB)

# change to 1 (one) to disable file uploads 
$CGI::DISABLE_UPLOADS = 0; #1 disables uploads, 0 enables uploads

my $query = new CGI;

my $upload_dir = "../photos";

my $filename_characters = 'a-zA-Z0-9_.-';
my $file = $query->param("fileToUpload");
my ($filename,undef,$ext) = fileparse($file,qr{\..*});
	$filename =~ tr/ /_/;
	$filename =~ s/[^$filename_characters]//g;
	$filename .= $ext;

if ($filename =~ /^([$filename_characters]+)$/) {
   $filename = $1;
}
else{
   print $query->header(),
         $query->start_html(),
         'The filename is not valid. Filenames can only contain these characters: ',
         $filename_characters,
         $query->end_html;
   exit(0);
}  

my $upload_filehandle = $query->upload("fileToUpload");
open (UPLOADFILE, ">$upload_dir/$filename") or die "$!";
binmode UPLOADFILE;
while ( <$upload_filehandle> ) {
   print UPLOADFILE;
}
close UPLOADFILE;

print $query->header ( );
print <<END_HTML;
	<!DOCTYPE HTML>
	<html>
	<head>
		<title>Thank you.</title>
		<link rel="stylesheet" type="text/css" href="styles.css" /><!-- graydata.com -->
	</head>
	<body>
		<fieldset>
			<fieldset><legend>Upload submitted</legend>
				<br />
				The file upload form has been submitted.<br /><br />
				<form id="generateThumbnails" action="thumbs.cgi">
					<input type="submit" name="Submit" value="Your photo has been uploaded, now click this button to run the thumbnail generator and preview all of the images that you have uploaded so far." />
				</form>
			</fieldset>
		</fieldset>
		<br />
	</body>
	</html>
END_HTML
