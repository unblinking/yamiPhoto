#!/usr/bin/perl

use strict;
use warnings;
use CGI;
use CGI::Carp qw/fatalsToBrowser/;
use Image::Magick;
use File::Basename;

my $query = new CGI;
my $dir = "../photos";	# relative location of photo directory from this cgi
my @files = <$dir/*>;
my $image;
my $links = '';

foreach (@files)	{		# for every photo in the photo directory
	$_ =~ s!$dir/!!gi;		# remove path from filename
	if ($_ ne "thumbs") {
			$image = Image::Magick->new;
			$image->Read("$dir/$_");
			$image->Set(Gravity => 'Center');
			$image->Resize(geometry => '64x64');
			$image->Extent(geometry => '64x64');
			$image->Write("$dir/thumbs/$_");
	$links .= "<a href=\"$dir/$_\"><img alt=\"$_\" src=\"$dir/thumbs/$_\" class=\"photos-images\" /></a>\n";
	}
}

$links.= "</table>";

print $query->header ( );
print <<END_HTML;
	<!DOCTYPE HTML>
	<html>
	<head>
		<title>Thank you.</title>
		<link rel="stylesheet" type="text/css" href="styles.css" />
	</head>
	<body>
		<fieldset>
			<fieldset><legend>Thumbnail Images Generated</legend>
				<br />
				Thumbnail images have been generated for all photos in the $dir directory.
				<br /><br />
				$links
				<br /><br />
				Go back to the <a href="index.cgi">File Manager</a> page.
			</fieldset>
		</fieldset>
	</body>
	</html>
END_HTML
