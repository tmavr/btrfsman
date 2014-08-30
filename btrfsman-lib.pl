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

1;