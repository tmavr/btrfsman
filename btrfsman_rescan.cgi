#!/usr/bin/perl
# btrfsmanscrub.cgi
# BTRFS Manager - Rescan Devices

require './btrfsman-lib.pl';

&ReadParse();

ui_print_header(undef, $text{'rescan_title'}, "", undef, 1, 1);

if($in){
  print $text{'txt_arg'}, $in, $text{'txt_p'};
}


$result = `btrfs device scan 2>&1`;
print $text{'rescan_cmd'};
print $text{'txt_p'}, $result;
print $text{'txt_p'};
print $text{'rescan_complete'};

ui_print_footer('/', 'Webmin index', '', 'Module menu');
