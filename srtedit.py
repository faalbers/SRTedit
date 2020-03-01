from srtparse.parser import SrtParser

# First copy the SRT file that you want to edit in this directory so the script can find it
# After you make the proper changes below, run the command 'python srtedit.py' to run the script

# rename file name to your file
srt = SrtParser.parse('DJIG0004.srt')

# If no format lines are added, the default fields are used in a column
# The following example takes the existing named fields and replace it with your string.
# It creates a line for each add. The new=True in the first command will remove the existing default
# fields first before adding new lines.
# @<original field name>@ will take the original value of that field. For examble @uavBat@ will be
# replaced with the a tual value of that field. It will remove all non digit characters of that value.
# For example, 12.4V will become just 12.4.
# It can also contain Python expressions that will be evaluated as seen below in this example.
srt.add_formatLine('Delay: @delay@ ms', new=True)
srt.add_formatLine('BitRate: @bitrate@ Mbps')
srt.add_formatLine('SignalQ: @signal@/4')
srt.add_formatLine('Time: @int(flightTime/60)@:@flightTime - ( int(flightTime/60) * 60 )@')
srt.add_formatLine('Bat: @uavBat@ V')
srt.add_formatLine('Cell: @int( uavBat * 100 /uavBatCells ) / 100@ V')

# uncomment following line to also see a printout on the screen
#print(srt)

# rename file name to be saved to your file
srt.save('DJIG0004_edit.srt')

print('Done')
