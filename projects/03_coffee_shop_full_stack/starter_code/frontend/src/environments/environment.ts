/* @TODO replace with your variables
 * ensure all variables on this page match your project
 */

export const environment = {
  production: false,
  apiServerUrl: 'http://127.0.0.1:5000', // the running FLASK api server url
  auth0: {
    url: 'dev-0s6akm4i.us.auth0.com', // the auth0 domain prefix
    audience: 'aimedjobia', // the audience set for the auth0 app
    clientId: 'cPqAGcJ6eJ2ts5hBw5dVBF3Yk2ZddhW8', // the client id generated for the auth0 app
    callbackURL: 'http://localhost:8100', // the base url of the running ionic application. 
  }
};
