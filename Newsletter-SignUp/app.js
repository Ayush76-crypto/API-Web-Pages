const express = require("express");
const bodyParser = require("body-parser");
const request = require("request");

const app = express();
const port = 3000;

app.use(express.static("public"));
app.use(bodyParser.urlencoded({ extended: true }));

app.get("/", (req, res) => {
  res.sendFile(__dirname + "/signup.html");
});

app.post("/", (req, res) => {

    var firstName = req.body.fName;
    var lastName = req.body.lName;
    var email = req.body.email;

    var data = {
      members: [
        {
          email_address: email,
          status: "subscribed",
          merge_fields: {
            FNAME: firstName,
            LNAME: lastName
          }
        }
      ]
    };

    var jsondata = JSON.stringify(data);

    var options = {
      url: "https://us5.api.mailchimp.com/3.0/lists/15bb107e89",
      method: "POST",
      headers: {
        "Authorization": "Ayush85 501eb0f183b00ec7136d5186c4dc3725-us5"
      },
      body: jsondata
    };

    request(options, function(error, response, body) {
      if (error) {
        // console.log(error);
        res.sendFile(__dirname + "/failure.html");
      } else {
        // console.log(response.statusCode);
        if (response.statusCode === 200) {
          res.sendFile(__dirname + "/success.html");
        } else {
          res.sendFile(__dirname + "/failure.html");
        }
      }
    });

    // console.log(firstName,lastName,email);

});

app.post('/failure', function(req, res) {
  res.redirect("/");
})


app.listen(port, () => {
  console.log(`Server is running at:- http://localhost:${port}`);
});

// 501eb0f183b00ec7136d5186c4dc3725-us5
// List ID :- 15bb107e89