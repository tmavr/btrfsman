#!/usr/bin/perl
# btrfsman_label.cgi
# BTRFS Manager - Label Devices

require './btrfsman-lib.pl';
&ReadParse();

ui_print_header(undef, $text{'label_title'}, "", undef, 1, 1);

if($in){
  print $text{'txt_arg'}, $in, $text{'txt_p'};
}

$act = $in{'act'};
$mountpoint =  $in{'mountpoint'};
$newlabel = $in{'newlabel'};

if ((length $newlabel) > 255){
	print "label too long";
}
if ($newlabel =~ /[ %&<>!\x27\x60\x3B\x3A\x\n\r\l]/) {
	print "not a safe string to use as label";
	
}

if (($act eq 'label') && ($mountpoint) ) {
  if ($newlabel) {
    print "Taking Action Executing Command:#", $text{'txt_p'};
    print "btrfs fi label $mountpoint $newlabel", $text{'txt_p'};
    print $text{'label_changed'}, $text{'txt_p'} ;
  }
}
else{
	showfs();
	labelmenu();
}
ui_print_footer('/', 'Webmin index', '', 'Module menu');


=head1 balancemenu

Display filesystems - info

=cut
sub showfs{
	  print $text{'index_btrfslogical'};

  $result = `btrfs fi show 2>&1`;
  $result =~ s/^\s+//; 
  $result =~ s/^\r+//; 
  $result =~ s/^\n+//; 
  $result =~  s/\n/<br>/g;
  print ui_hidden_table_start( $text{'index_btrfsfis'}, "width=100%", 1, 1 );
  print ui_table_row( $result);
  print ui_hidden_table_end();

  #$result =~ s/^\s+//; 
  @fsa = split /Label/, $result;
  print $text{'index_youhave1'}, (scalar (@fsa) - 1), $text{'index_youhave2'};
  $did=1;
  for (1..scalar(@fsa)-1){
    #print $did, "#", @fsa[$did],"<p>";

    @splitres  =   split /\:/, @fsa[$did];
    #print "!1", @splitres[1], "<p>!2", @splitres[2], "<p>!3", @splitres[3],   "<p>";

    print ui_columns_start([$text{'index_fs'} ,""]);
    @label[$did] = @splitres[1];
    @label[$did] =~ s/uuid//g;
    @label[$did] =~ s/[\x27 ]//g;
    print ui_columns_row([$text{'index_lb'}, @label[$did] ]);

    @uuid[$did] = @splitres[2];
    @uuid[$did] =~ s/^\s//;
    @uuid[$did] =~ s/<br>(.*)//;
    print ui_columns_row([$text{'index_uu'}, @uuid[$did] ]);

    @bdevices[$did] = @splitres[2];
    @bdevices[$did] =~ s/(.*)Total//;
    @bdevices[$did] =~ s/Btrfs(.*)//;
    @bdevices[$did] =~ s/<br>$//g;
    @bdevices[$did] =~ s/<br>$//g;
    print ui_columns_row([$text{'index_dev'}, @bdevices[$did] ]);

    print ui_columns_end();

    $did++;
  }
}

=head1 labelmenu

Display label menu

=cut
sub labelmenu {
  print $text{'label_mounted_h'};
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

    if ($result =~ /no stats available/) {
      print ui_columns_row([$text{'index_warn'}, $text{'index_warnnoscrub'}]);
    }
    print ui_columns_end();

    print ui_buttons_start();
    print ui_buttons_row("btrfsman_label.cgi",  $text{'label_bt_change'},  $text{'label_bt_change_help'}, ui_hidden('act', 'label'), ui_hidden('mountpoint', @mountedrive[$did]), ui_textbox('newlabel','NewLabel'));
    print ui_buttons_end();

    print "<p><p>";

    $did++;
  }
}
