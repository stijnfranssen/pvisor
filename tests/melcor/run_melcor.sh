# Create and cd the temp folder
rm -rf temp
mkdir -p temp
cd temp

# Remove old output
rm *.DIA *.OUT *.RST *.PTF *.MES *.STP *.SCN 2> /dev/null

exit

# Copy input
MODELNAME=MODEL
cp ../${MODELNAME} ./
cp ../*.MEL ./

# Location of the melcor Executable
EXEDIR=/software/TH-codes/MELCOR_2

# Run MELCOR
${EXEDIR}/melgen *.MEL
${EXEDIR}/melcor *.MEL

# Move output to test folder
cp *.PTF ../