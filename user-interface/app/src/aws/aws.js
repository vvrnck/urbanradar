// import { fromCognitoIdentityPool } from "@aws-sdk/credential-providers";
// import { GetObjectCommand, S3Client } from '@aws-sdk/client-s3';
// import * as AWS from 'aws-sdk';

// const credentials = fromCognitoIdentityPool({
//   identityPoolId: process.env.VUE_APP_AWS_IDENTITY_POOL_ID,
//   clientConfig: { region: process.env.VUE_APP_AWS_BUCKET_REGION },
// });

// const s3Client = new S3Client({ 
//   apiVersion: "2006-03-01",
//   region: process.env.VUE_APP_AWS_BUCKET_REGION,
//   credentials
// });

// AWS.config.region = process.env.VUE_APP_AWS_BUCKET_REGION; // Region
// AWS.config.credentials = new AWS.CognitoIdentityCredentials({
//     IdentityPoolId: process.env.VUE_APP_AWS_IDENTITY_POOL_ID,
//     RoleArn: process.env.VUE_APP_AWS_ROLE_ARN,
// });

// const addPhoto = async (file, fileName) => {
//     // Use S3 ManagedUpload class as it supports multipart uploads
//     var upload = new AWS.S3.ManagedUpload({
//       params: {
//         Bucket: process.env.VUE_APP_AWS_BUCKET_NAME,
//         Key: `media/${fileName}`,
//         Body: file
//       }
//     });
  
//     var promise = upload.promise();
  
//     return promise;
// }

// const streamToString = (stream) => {
// 	return new Promise((resolve, reject) => {
// 	  if (stream instanceof ReadableStream === false) {
// 		reject(
// 		  "Expected stream to be instance of ReadableStream, but got " +
// 			typeof stream
// 		);
// 	  }
// 	  let text = "";
// 	  const decoder = new TextDecoder("utf-8");
  
// 	  const reader = stream.getReader();
// 	  const processRead = ({ done, value }) => {
// 		if (done) {
// 		  // resolve promise with chunks
		  
// 		  // resolve(Buffer.concat(chunks).toString("utf8"));
// 		  resolve(text);
// 		  return;
// 		}
  
// 		text += decoder.decode(value);
  
// 		// Not done, keep reading
// 		reader.read().then(processRead);
// 	  };
  
// 	  // start read
// 	  reader.read().then(processRead);
// 	});
//   };

// const download = async (url) => {
// 	const urlArray = url.split("/");

// 	// pattern: https://domain/folder/image
// 	const objectName = urlArray[urlArray.length - 1];
// 	const objectFolder = urlArray[urlArray.length - 2];

// 	const bucketParams = {
// 		Bucket: process.env.VUE_APP_AWS_BUCKET_NAME,
// 		Key: `${objectFolder}/${objectName}`,
// 	}

//   	try {
// 		const command = new GetObjectCommand(bucketParams);

// 		// // Get the object} from the Amazon S3 bucket. It is returned as a ReadableStream.
// 		const data = await s3Client.send(command);		

// 		const bodyContents = await streamToString(data.Body);

//     	return bodyContents;
		
//   	} catch (error) {
//       	const { requestId, cfId, extendedRequestId } = error.$metadata;
  		
// 		return null;
//   	}
// }



// export { addPhoto, s3Client, download };