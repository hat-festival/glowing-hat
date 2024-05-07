OUTFILE=${1}
shift


ruby -e "require 'nineteen/eighty/two' ; require 'yaml' ; File.write('/opt/output/${OUTFILE}.yaml', YAML.dump(Nineteen::Eighty::Two::Spectrum['${@}  ']))"
