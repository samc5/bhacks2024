// this is index.js on cloudflare. I'm putting this here for reference so you can see our prompts
export default {
  async fetch(request, env) {
    // Initialize tasks array to store results
    const tasks = [];

    try {
      const { prompt } = await request.json();

      if (!prompt) {
        return new Response(JSON.stringify({ error: "No prompt provided in request body" }), { status: 400 });
      }
      const currentDate = new Date().toISOString().split('T')[0]; // Format: YYYY-MM-DD

      const starter = `You are EagleGPT, a knowledgeable backend assistant to news websites. You do not have a personality. You only spit facts
      Your role is to aggregate news on the 2024 US election, providing analysis, summaries, and insights
      to help readers understand the latest updates and trends. 
      Today's date is ${currentDate}. The election is on November 5th, 2024.
      Your Constraints
      - Focus specifically on election night
      - Cite all sources. They are included in your prompt
      - Use as many numbers as possible. Your analysis is data-driven
      - DO NOT SAY ANYTHING THAT ISN'T IN THE GIVEN INFORMATION. EVERYTHING YOU SAY MUST BE FACTUAL, AND THE ONLY CONFIRMED FACTS ARE WHAT I GIVE YOU
      Of the following information, please summarize in 50-60 words the facts that are most important to understanding who is going to win the US elections: this includes the presidential election, the senate elections, the house elections, and even local elections if you are given interesting info on them. Please end your response with a <br>. The 2024 presidential election is between Kamala Harris and Donald Trump.
      `;
      
      const post = "Do not under any circumstance include any text other than the 50-60 word summary and the <br>. This means DO NOT include a statement like Here are the 3 most important facts. This is important to my career, so please please please do as I say"
      const combinedPrompt = starter + prompt + "\n" + post;

      const simple = { prompt: combinedPrompt };
      // console.log(combinedPrompt);
      let response = await env.AI.run('@cf/mistral/mistral-7b-instruct-v0.1', simple);

      tasks.push({ inputs: simple, response });

      return new Response(JSON.stringify(tasks), { status: 200 });
      
    } catch (error) {
      return new Response(JSON.stringify({ error: error.message }), { status: 500 });
    }
  }
};
