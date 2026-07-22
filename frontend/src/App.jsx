import { useState } from "react";
import axios from "axios";
import "./App.css";


function App() {


  const [prompt, setPrompt] = useState("");

  const [messages, setMessages] = useState([]);

  const [loading, setLoading] = useState(false);



  // -----------------------------
  // Ask AI Function
  // -----------------------------

  const askAI = async () => {


    if (!prompt.trim()) {

      alert("Please enter a disaster-related question");

      return;

    }



    const userMessage = prompt;



    setMessages((prev) => [

      ...prev,

      {

        role: "user",

        text: userMessage

      }

    ]);



    setPrompt("");

    setLoading(true);



    try {



      const response = await axios.post(

        "http://127.0.0.1:8000/chat",

        {

          prompt: userMessage

        }

      );



      setMessages((prev) => [

        ...prev,

        {

          role: "ai",

          text: response.data.answer,

          disaster: response.data.disaster,

          severity: response.data.severity,

          sources: response.data.sources

        }

      ]);




    } catch(error) {



      console.error(error);



      setMessages((prev)=>[

        ...prev,

        {

          role:"ai",

          text:
          "❌ Unable to connect with AI server. Please make sure backend is running."

        }

      ]);



    }



    finally {


      setLoading(false);


    }


  };






  // -----------------------------
  // Clear Chat
  // -----------------------------

  const clearChat = ()=>{


    setMessages([]);


  };





  // -----------------------------
  // Copy Response
  // -----------------------------

  const copyText = (text)=>{


    navigator.clipboard.writeText(text);


    alert("Response copied!");

  };





  return (



    <div className="app">



      <header>


        <h1>
          🌍 AI Disaster Management System
        </h1>



        <p>
          AI-powered emergency analysis and disaster assistance
        </p>



        <button
          className="clear-btn"
          onClick={clearChat}
        >

          🧹 Clear Chat

        </button>



      </header>





      <div className="chat-container">



        <div className="chat-box">



          {

          messages.length === 0 ?



          (

            <p className="welcome">

              Ask me anything about earthquakes,
              floods, cyclones, wildfire, tsunami,
              landslides or disaster safety.

            </p>


          )

          :


          (


            messages.map((msg,index)=>(



              <div

                key={index}

                className={

                  msg.role==="user"

                  ?

                  "user-message"

                  :

                  "ai-message"

                }


              >



                <strong>


                  {msg.role==="user"

                  ?

                  "👤 You"

                  :

                  "🤖 DisasterAI"

                  }


                </strong>





                {


                msg.role==="ai" &&

                (

                  <div className="metadata">



                    <p>

                      🌎 Disaster:

                      {" "}

                      {msg.disaster}

                    </p>




                    <p>

                      🚨 Severity:

                      {" "}

                      {msg.severity}

                    </p>



                  </div>

                )


                }







                <p>

                  {msg.text}

                </p>





                {


                msg.role==="ai"

                &&

                (

                  <button

                    className="copy-btn"

                    onClick={()=>

                      copyText(msg.text)

                    }

                  >

                    📋 Copy

                  </button>

                )


                }







                {


                msg.role==="ai"

                &&

                msg.sources

                &&

                msg.sources.length>0

                &&

                (

                  <div className="sources">



                    <h4>

                      📚 Sources Used

                    </h4>




                    {


                    msg.sources.map(

                      (source,i)=>(


                        <p key={i}>

                          📄 {source}

                        </p>


                      )

                    )


                    }




                  </div>

                )


                }




              </div>



            ))


          )

          }







          {


          loading &&

          (

            <div className="ai-message">


              <strong>

                🤖 DisasterAI

              </strong>


              <p>

                Analyzing disaster information...

              </p>


            </div>


          )


          }



        </div>







        <div className="input-area">



          <textarea


            value={prompt}


            onChange={(e)=>

              setPrompt(e.target.value)

            }


            placeholder=
            "Ask your disaster-related question..."


          />





          <button

            onClick={askAI}

            disabled={loading}


          >


            {

            loading

            ?

            "Processing..."

            :

            "Ask AI"

            }



          </button>





        </div>





      </div>





    </div>



  );


}



export default App;