const { correct } = require("@ipmanlk/subasa-api");
const fs = require('fs')

const text = "මථකය (ස්මෘතිය) යනු ජීවියෙකු තුළ තොරතුරු ගබඩා කිරීමට සහ ඉන්පසුව එම තොරතුරු ණැවත එලි දැක්වීමට ඇති හැකියාවයි.";
var counter = 0;
fs.readFile('Data/combined all names - cleaned - validation.txt', 'utf8' , (err, fileData) => {
  if (err) {
    console.error(err)
    return
  }
  correct(fileData).then(data => {
    //console.log("corrected text: ", data.text);
    console.log("corrections: ", data.corrections);
    //console.log(data.corrections);
    // fs.writeFile('Benchmarking spell checkers/subasa.txt', JSON.stringify(data.corrections), err => {
    //     if (err) {
    //       console.error(err)
    //       return
    //     }
    //     //file written successfully
    //   })
  })
})