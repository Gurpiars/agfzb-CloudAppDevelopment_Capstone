const express = require('express');
const app = express();
const port = process.env.PORT || 3000;
const Cloudant = require('@cloudant/cloudant');

async function dbcloudantconnect(){
    try{
        const cloudant = Cloudant({
            plugins:{ iamauth:{ iamApiKey:"lzfHf63-jWFoa-fpn2kKuqXBULiCUimvzrco2anaM033" }},
            url:"https://8eeb3700-29c8-4207-b533-59975ae493bd-bluemix.cloudantnosqldb.appdomain.cloud",
        });
        const db = cloudant.use('dealerships');
        console.info("Successfully connected to the database")
        return db;
    }catch(err){
        console.error('Error occured', err.mesage)
        throw err;
    }
}

let db;

(async()=>{
    db = await dbcloudantconnect();
})();

app.use(express.json());

app.get('/dealerships/get' , async(req,res)=>{
    const{state, id} = req.query;
    const selector ={};

    if (state){
        selector.state=state;
    }
    if (id){
        selector.id=parseInt(id);
    }

    const queryoptions = {
        selector,
        limit:10,
    }
    db.find(queryoptions, (err, body) => {
        if (err) {
            console.error('Error fetching dealerships:', err);
            res.status(500).json({ error: 'An error occurred while fetching dealerships.' });
        } else {
            const dealerships = body.docs;
            res.json(dealerships);
        }
    });
});

app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
}); 