#!/usr/bin/perl

use strict;
use warnings;
use utf8;

my $flag;
my @output_lines;
my @reg_list;

unless ( defined $ARGV[0] ) { #  使い方間違ってるよ
  print STDERR "usage: $0 <CIRCUIT_FILE> \n";
  print STDERR "output is STDOUT.\n";
  exit 1;
}

my $CIRCUIT_FILE = shift @ARGV;  ## ファイルの存在確認
unless ( -f $CIRCUIT_FILE ){
  print STDERR "The \'$CIRCUIT_FILE'\ is not file!\n";
  exit 1;
}

open CIRCUIT, '<', $CIRCUIT_FILE; # ファイル読み込み
local $/ = ';'; # デミリタはセミコロンです.
my @lines = <CIRCUIT>;
close CIRCUIT;

my @port_list;

foreach ( @lines ){
  if ( /^\s*module\s+\w+\s*\(([,\.\w\s\{\}\(\)]+)\)\s*;$/ ){
    my @tmp = split( /,/, $1 );
    foreach my $port ( @tmp ){
      if ( $port =~ /\.\w+\(\{(\w+)/ ){
        $port = $1;
      }
      else {
        $port =~ s/\s+|\}|\)//g;
      }
      push @port_list, $port;
    }
    push @output_lines, $_; # FD2を含まない行は表示するお
    # print STDERR join( "\n", @port_list ) . "\n";
  }
  elsif ( /^\s*FD2\s+/ ){ # FD2だけぶっこ抜く
    my ( $unit, $d, $q, $qn ); # 変数定義
    $_ =~  /^\s*FD2\s+(\w+)/; # unit name
    $unit = $1;

    $_ =~ /\.D\((\w+\[?\d*\]?)\)/; # wire connected with D port
    $d = $1;

    if ( $_ =~ /\.Q\((\w+\[?\d*\]?)\)/ ){ # wire connected with Q port
      if ( grep( /^$1$/ , @port_list ) ){
        print STDERR "Unit '$unit' has a primary port '$1'\n";
      }
      $q = $1;
    } else {
      $q = ''; # warnings対策
    }

    # wire connected with QN port
    if ( $_ =~ /\.QN\((\w+\[?\d*\]?)\)/ ){
      if ( grep( /^$1$/ , @port_list ) ){
        print STDERR "Unit '$unit' has a primary port '$1'\n";
      }
      $qn = $1;
    } else {
      $qn = ''; # Warning対策
    }

    # チェックしたいとき
    # print STDERR "$unit / $d / $q / $qn\n";

    # unless ( ( $d eq $q ) or ( $d eq $qn ) ){ # 変態なケースが存在した
    my $reg = { 'unit' => $unit, 'd' => $d, 'q' => $q, 'qn' => $qn };
    push @reg_list, $reg;
    # }

  } else {
    push @output_lines, $_; # FD2を含まない行は表示するお
  }
}


$flag = 0;
foreach ( @output_lines ){ # cclizeした回路に
  if ( $flag == 0 ) {
    if ( /^\s*module/ ){ # port宣言
      $flag = 1; #  次のふぇーずへ
      $_ =~ s/\s*\)\s*;//g; # 最後の括弧閉じとセミコロンを削除
      $_ .= ', ' . SequencePortDef( \@reg_list, 'd' );
      $_ .= ', ' . SequencePortDef( \@reg_list, 'q' );
      $_ .= ");\n\n"; # 〆
    }
  } elsif ( $flag == 1 ) {
    if ( /^\s*input/ ){ # input/output宣言を追加
      $flag = 2; #  次のふぇーず
      print "\n\n"; #なんかコレ入れない見難い
      my $ffin  = "  input "; # input宣言
      $ffin    .= SequencePortDef( \@reg_list, 'q' ) . ";\n";
      print $ffin;
      my $ffout = "  output "; # output宣言
      $ffout   .= SequencePortDef( \@reg_list, 'd' ) . ";\n";
      print $ffout;
    }
  } elsif ( $flag == 2 ) {
    if ( /^\s+\w+\s*\w+\s*\(/ ){
      $flag = 3;
      print "\n\n"; #なんかコレ入れない見難い

      foreach my $reg ( @reg_list ){
        # qのassign
        if ( $reg->{'q'}  ne '' ) { # qがあるとき
          print "  assign " .
          $reg->{'q'}  . " = "  . PortDefName( $reg, 'q' ) . ";\n";
        }

        # qnのassign
        if ( $reg->{'qn'} ne '' ){ # qnがあるとき
          print "  assign " .
          $reg->{'qn'} . " = ~" . PortDefName( $reg, 'q' ) . ";\n";
        }

        # dのassign  ぜったいあるから
        print "  assign " .  PortDefName( $reg, 'd' ) . " = " . $reg->{'d'} . ";\n";
      }

      print "\n";
    }
  } else {  } # 全てのふぇーず終了
  print $_; #
}

sub SequencePortDef {

  my $reg_list_ref  = shift;
  my $type          = shift;
  my $port_def_line = '';

# make port list
  foreach my $reg ( @$reg_list_ref ){
    $port_def_line .= PortDefName( $reg, $type ) . ', ';
  }

  chop( $port_def_line ); # セミコロン削除
  chop( $port_def_line ); # スペース削除

  return $port_def_line;
}

sub PortDefName {

  my $reg  = shift;
  my $type = shift;
  my $port_def;
  my ( $wire, $bit );

  if ( $type eq 'd' ){ # D系
    $type = 'd';
  } else { # Q系
    if ( $reg->{'q'} ne '' ) { #Qが定義されている
      $type = 'q';
    } else { # Qが定義されていない
      $type = 'qn';
    }
  }

  if ( $reg->{"$type"} =~ /(\w+)\[?(\d*)\]?/ ){
    $wire = $1;
    $bit  = $2;
    $port_def = $reg->{'unit'} . '_' . $type . '_' . $wire . '_' . $bit;
  } else {
    $port_def = $reg->{'unit'} . '_' . $type . '_' . $reg->{"$type"};
  }

  return $port_def;
}


