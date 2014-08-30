#!/usr/bin/perl
# index.cgi
# BTRFS Manager main program

require './btrfsman-lib.pl';
&init_config();
#ui_print_header(undef, $text{'index_title'}, "", undef, 1, 1);
ui_print_header(undef, $text{'index_subtitle'}, "", undef, 1, 1);

if (has_command($config{'btrfs_cmd'})){
		
  print ui_columns_start([$text{'index_btrfstoolsinfo_h'}, ""]);

  $result = `which btrfs  2>&1`;
  
  if ($result =~ /$config{'btrfs_cmd'}$/) {
    print ui_columns_row([ $text{'index_foundbtrfs'}, $result]);
    $result = `btrfs --version 2>&1`;
    print ui_columns_row([$text{'index_version'}, $result]);
    print $text{'txt_p'};

    $btrfsprog = 1;
  }
  else {
    print ui_columns_row([$text{'index_notfoundbtrfs'}, $text{'txt_error'}]);
  }
  print ui_columns_end();
}
else {
	print $text{'txt_error'}, $text{'txt_p'}, $text{'index_noconfig'};
}


if ($btrfsprog){

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
  print ui_buttons_start();
  print ui_buttons_row("btrfsman_rescan.cgi",  $text{'index_bt_rescan'},  $text{'index_bt_rescan_help'} );
  print ui_buttons_row("btrfsman_mkfs.cgi", $text{'index_bt_create'}, $text{'index_bt_create_help'});
  print ui_buttons_end();


  print $text{'index_mounted_h'};

  print ui_hidden_table_start($text{'index_mountgrep'}, "width=100%", 2,2 );
  $result = `mount |grep btrfs`;
  $result =~  s/\n/<br>/g;
  print  ui_table_row($result);
  print ui_hidden_table_end();


  @splitres = split /<br>/, $result;
  print $text{'index_youhave1'}, scalar (@splitres), $text{'index_youhave3'};

  $did=0;
  for (@splitres){
    print ui_columns_start([ @splitres[$did], ""]);
    $drivea = @splitres[$did];
    @driveb = split /on /, $drivea;
    @drivec = split / /, @driveb[1];
    @mountedrive[$did] =  @drivec[0]; 
    #print "A:", $drivea, "B:", @driveb[1], "C:", @drivec[0], "mount:", @mountedrive[$did], "<p>";
  
    print ui_columns_row([$text{'index_mountp'}, @mountedrive[$did]]) ; 
    $result = `btrfs fi df @mountedrive[$did]`;
    $result =~  s/\n/<br>/g;
    print ui_columns_row([$text{'index_btrfsdf'}, $result]);

 
    $result = `btrfs scrub status @mountedrive[$did]`;
    $result =~  s/\n/<br>/g;
    print ui_columns_row([ $text{'index_btrfsss'} , $result]);

    if ($result =~ /no stats available/) {
      print ui_columns_row([$text{'txt_warn'}, $text{'txt_warn_noscrub'}]);
    }

    $result = `btrfs balance status @mountedrive[$did]`;
    $result =~  s/\n/<br>/g;
    print ui_columns_row([ $text{'index_btrfsbal'} , $result]);


 
    $result = `btrfs replace status @mountedrive[$did] -1`;
    $result =~  s/\n/<br>/g;
    print ui_columns_row([$text{'index_btrfsrs'}, $result]);
 

    $result = `btrfs subvolume list @mountedrive[$did]`;
    $result =~  s/\n/<br>/g;
    print ui_columns_row([$text{'index_btrfssl'}, $result]);
    
    $result = `btrfs device stats @mountedrive[$did]`;
    $result =~  s/\n/<br>/g;
    print ui_columns_row([$text{'index_btrfsds'}, $result]);
 
 
    $did++;
    print ui_columns_end();
  }

  print ui_buttons_start();
  print ui_buttons_row("btrfsman_label.cgi", $text{'index_bt_label'}, $text{'index_bt_label_help'});
  print ui_buttons_row("btrfsman_scrub.cgi",$text{'index_bt_scrub'}, $text{'index_bt_scrub_help'});
  print ui_buttons_row("btrfsman_defrag.cgi",$text{'index_bt_defrag'}, $text{'index_bt_defrag_help'}); 
  print ui_buttons_row("btrfsman_balance.cgi", $text{'index_bt_bal'}, $text{'index_bt_bal_help'});
  print ui_buttons_row('btrfsman_sub.cgi',  $text{'index_bt_sub'}, $text{'index_bt_sub_help'});
  print ui_buttons_row('btrfsman_arr.cgi',  $text{'index_bt_arp'}, $text{'index_bt_arp_help'});
  print ui_buttons_end();


  print $text{'index_latestlogs_h'};

  $result = `dmesg |grep -i btrfs`;
  print ui_hidden_table_start($text{'index_latestlogs_d'}, "width=100%",3,3 );
  $result =~ s/^\s+//;
  $result =~ s/^\r+//;
  $result =~ s/^\n+//;
  $result =~  s/\n/<br>/g;
  print ui_table_row( $result);
  print ui_hidden_table_end();

  $result = `tail -n 1000 /var/log/messages |grep -i btrfs`;
  print ui_hidden_table_start( $text{'index_latestlogs_m'}, "width=100%",4,4 );
  $result =~ s/^\s+//;
  $result =~ s/^\r+//;
  $result =~ s/^\n+//;
  $result =~  s/\n/<br>/g;
  print ui_table_row( $result);
  print ui_hidden_table_end();

} #end_if ($btrfsprog)

#ui_print_footer("/", $text{'index_foot'});
ui_print_footer('/', 'Webmin index', '', 'Module menu');


