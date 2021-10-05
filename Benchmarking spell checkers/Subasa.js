const { correct } = require("@ipmanlk/subasa-api");
const fs = require('fs')

const text = "මථකය (ස්මෘතිය) යනු ජීවියෙකු තුළ තොරතුරු ගබඩා කිරීමට සහ ඉන්පසුව එම තොරතුරු ණැවත එලි දැක්වීමට ඇති හැකියාවයි.";

correct(text).then(data => {
    console.log("corrected text: ", data.text);
    console.log("corrections: ", data.corrections);
    //console.log(typeof data.corrections);
    fs.writeFile('Benchmarking spell checkers/subasa.txt', JSON.stringify(data.corrections), err => {
        if (err) {
          console.error(err)
          return
        }
        //file written successfully
      })
});