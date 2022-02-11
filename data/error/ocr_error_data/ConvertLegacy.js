var convert  = require("sinhala-unicode-coverter");
const fs = require('fs')

fs.readFile('Data/combined all names - cleaned - validation.txt', 'utf8' , (err, data) => {
  if (err) {
    console.error(err)
    return
  }
  const b = convert.unicodeToDlManel(data)


fs.writeFile('Data/legacy - validation.txt', b, err => {
    if (err) {
      console.error(err)
      return
    }
    //file written successfully
  })
})