var convert  = require("sinhala-unicode-coverter");
const fs = require('fs')

fs.readFile('Data/Addresses/addresses - cleaned.txt', 'utf8' , (err, data) => {
  if (err) {
    console.error(err)
    return
  }
  const b = convert.unicodeToDlManel(data)


fs.writeFile('Data/legacy - addresses.txt', b, err => {
    if (err) {
      console.error(err)
      return
    }
    //file written successfully
  })
})