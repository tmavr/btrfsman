#!/usr/bin/perl
# btrfsman_defrag.cgi
# BTRFS Manager - Defrag Filesystem

require './btrfsman-lib.pl';
&ReadParse();

ui_print_header(undef, $text{'defrag_title'}, "", undef, 1, 1);

if($in){
  print $text{'txt_arg'}, $in, $text{'txt_p'};
}

$act = $in{'act'};
$point =  $in{'point'};
$opt = $in{'opt'};

if ($point =~ /[ %&<>!\x27\x60\x3B\x3A\x\n\r\l]/) {
	print "not a safe string to use as directory";
}

if (($act eq 'defrag') && ($point) ) {
  if ($point) {
    $cmd = "btrfs fi defrag $opt $point 2>&1";
    print  $text{txt_executing}, $cmd, $text{'txt_p'};
    $result=`$cmd`;
    print $cmd, $text{'txt_p'}, $text{'defrag_started'}, $text{'txt_p'} ;
  }
}
else{
	defragmpmenu();
	defragfilemenu();
}
ui_print_footer('/', 'Webmin index', '', 'Module menu');





sub defragmpmenu {
  print $text{'label_defragmp_h'};
  $result = `mount |grep btrfs`;
  $result =~  s/\n/<br>/g;
	
  @splitres = split /<br>/, $result;
  print $text{'index_youhave1'}, scalar (@splitres), $text{'index_youhave3'};
  $did=0;
  for (@splitres){
    print ui_columns_start([ @splitres[$did], ""]);
    $drivea = @splitres[$did];
    @driveb = split /on /, $drivea;
    @drivec = split / /, @driveb[1];
    @mountedrive[$did] =  @drivec[0];
    print ui_columns_row([$text{'index_mountp'}, @mountedrive[$did]]) ;


    print ui_columns_end();

    print ui_buttons_start();
    print ui_buttons_row("btrfsman_defrag.cgi",  $text{'label_bt_defragstartmp'},  $text{'label_bt_defragstartmp_help'}, ui_hidden('act', 'defrag'), ui_hidden('point', @mountedrive[$did]), ui_textbox('options','-r'));
    print ui_buttons_end();

    print "<p><p>";

    $did++;
  }
}


sub defragfilemenu{
	print $text{'label_defragfile_h'};
	print ui_buttons_start();
  print ui_buttons_row("btrfsman_defrag.cgi",  $text{'label_bt_defragstartfile'},  $text{'label_bt_defragstartfile_help'}, ui_hidden('act', 'defragfile'), ui_filebox('file'), ui_textbox('options','-r'));
  print ui_buttons_end();
	
	
	
}

	