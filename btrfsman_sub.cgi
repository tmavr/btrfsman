#!/usr/bin/perl
# btrfsman_sub.cgi
# BTRFS Manager - Subvolume Management

require './btrfsman-lib.pl';
&ReadParse();

ui_print_header(undef, $text{'sub_title'}, "", undef, 1, 1);

if($in){
  print $text{'txt_arg'}, $in, $text{'txt_p'};
}

$act = $in{'act'};
$volume =  $in{'volume'};
$opt = $in{'opt'};


if ($volume =~ /[ %&<>!\x27\x60\x3B\x3A\x\n\r\l]/) {
	print "not a safe mountpoint";
}

if (($act) && ($volume) ) {
  #if ($newlabel) {
    print "NOT Taking Action Executing Command:#", $text{'txt_p'};
    print "NOT btrfs subvolume $act $volume $opt", $text{'txt_p'};
    print $text{'sub_operation'}, $text{'txt_p'} ;
  #}
}
else{
	
	submenu();
}
ui_print_footer('/', 'Webmin index', '', 'Module menu');


=head1 sunmenu

Display subvolume menu

=cut
sub submenu {
  print $text{'sub_h'};
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

    $result = `btrfs subvolume list @mountedrive[$did]`;
    $result =~  s/\n/<br>/g;
    print ui_columns_row([$text{'index_btrfssl'}, $result]);
  
    print ui_columns_end();

    print ui_buttons_start();
    
    if ($result){
    	print ui_buttons_row("btrfsman_sub.cgi",  $text{'sub_bt_delete'},  $text{'sub_bt_delete_help'}, ui_hidden('act', 'subvolume delete'), ui_hidden('volume', @mountedrive[$did]), ui_textbox('opt',''));
    }
    print ui_buttons_row("btrfsman_sub.cgi",  $text{'sub_bt_create'},  $text{'sub_bt_create_help'}, ui_hidden('act', 'subvolume create'), ui_hidden('volume', @mountedrive[$did]));
  
    print ui_buttons_end();

    print $text{'txt_p'};

    $did++;
  }
}
