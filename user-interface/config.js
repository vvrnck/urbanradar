const path = require('path');
const fs = require('fs');
const { generateRandomPassword, generateRandomUser } = require('./utils');

try {
    const user = generateRandomUser();
    const password = generateRandomPassword();

    const location = path.resolve("app");
    const data = "username:" + user + "\n" +
                 "password:" + password + "\n";

    fs.writeFile(path.join(location, 'account.txt'), data, (err) => {
        if (err) throw err;
    })
} catch(e) {
    console.error("Could not create account file!");
}
