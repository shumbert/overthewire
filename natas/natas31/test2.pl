#!/usr/bin/perl

my @lines = <test.csv>;
my $file = 'test.csv';
my @lines = <$file>;
print @lines;
#while (<$file>) {
#    print $_;
#}
