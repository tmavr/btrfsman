=head1 btrfsman-lib.pl

Functions for managing btrfs

=cut

BEGIN { push(@INC, ".."); };
use WebminCore;
&init_config();



=head1 show_parted

Display GNU parted -l

=cut
sub show_parted{

  if (has_command('parted')){
  	print ui_hidden_table_start($text{'arr_parted_h'}, "width=100%",4,4);

  	$result = `parted -l  2>&1`;
    $result =~ s/^\s+//;
    $result =~ s/^\r+//;
    $result =~ s/^\n+//;
    $result =~  s/\n/<br>/g;
  	print ui_table_row($result);
  		
  	print ui_hidden_table_end();
  		
  }else{
  	 print $text{'txt_error'}, $text{'txt_error_noparted'}, $text{'txt_p'};
  }
}







=head1 show_fs

Display filesystems - info

=cut
sub show_fs{

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

1;