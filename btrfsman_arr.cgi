#!/usr/bin/perl
# btrfsman_arr.cgi
# BTRFS Manager - Add Remove Replace Management

require './btrfsman-lib.pl';
&ReadParse();

ui_print_header(undef, $text{'arr_title'}, "", undef, 1, 1);

if($in){
  print $text{'txt_arg'}, $in, $text{'txt_p'};
}

$act = $in{'act'};
$dev =  $in{'dev'};
$mp = $in{'mp'};
$opt = $in{'opt'};


if ($dev =~ /[ %&<>!\x27\x60\x3B\x3A\x\n\r\l]/) {
	print "not a safe string";
}

if (($act) && ($mp) && ($dev)  ) {
  #if ($newlabel) {
    print "Taking Action Executing Command:#", $text{'txt_p'};
    print "btrfs device $act $dev $mp $opt", $text{'txt_p'};
    print $text{'arr_operation'}, $text{'txt_p'} ;
  #}
}
else{

  print $text{'sub_h'};	
  print $text{'arr_help'};
  
}
ui_print_footer('/', 'Webmin index', '', 'Module menu');

