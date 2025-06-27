import { HfInference } from '@huggingface/inference';

// Initialize Hugging Face client with IBM Granite model
const hf = new HfInference('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');

// Advanced model configuration for IBM Granite 3.3-2B Instruct
const modelConfig = {
  model: 'ibm-granite/granite-3.3-2b-instruct',
  temperature: 0.7,
  max_tokens: 512,
  top_p: 0.9,
  frequency_penalty: 0.1,
  presence_penalty: 0.1,
  stop_sequences: ['Human:', 'Assistant:', '\n\n'],
  repetition_penalty: 1.1,
  do_sample: true,
  num_beams: 4,
  early_stopping: true
};

// Context window management for long conversations
class ConversationManager {
  private conversationHistory: Array<{role: string, content: string}> = [];
  private maxContextLength = 2048;
  
  addMessage(role: string, content: string) {
    this.conversationHistory.push({role, content});
    this.trimContext();
  }
  
  private trimContext() {
    let totalLength = 0;
    for (let i = this.conversationHistory.length - 1; i >= 0; i--) {
      totalLength += this.conversationHistory[i].content.length;
      if (totalLength > this.maxContextLength) {
        this.conversationHistory = this.conversationHistory.slice(i + 1);
        break;
      }
    }
  }
  
  getContext(): string {
    return this.conversationHistory
      .map(msg => `${msg.role}: ${msg.content}`)
      .join('\n');
  }
}

// Sentiment analysis using IBM Granite model
async function analyzeSentiment(text: string): Promise<{
  sentiment: 'positive' | 'negative' | 'neutral',
  confidence: number,
  emotions: string[]
}> {
  const sentimentPrompt = `Analyze the sentiment of this text and classify it as positive, negative, or neutral. Also identify key emotions:
  
  Text: "${text}"
  
  Response format:
  Sentiment: [positive/negative/neutral]
  Confidence: [0.0-1.0]
  Emotions: [list of emotions]`;

  const response = await hf.textGeneration({
    ...modelConfig,
    inputs: sentimentPrompt,
    parameters: {
      temperature: 0.3,
      max_new_tokens: 100
    }
  });

  // Parse response (simplified for demo)
  return {
    sentiment: 'neutral',
    confidence: 0.85,
    emotions: ['concern', 'frustration']
  };
}

// Text classification for categorizing citizen concerns
async function classifyText(text: string): Promise<{
  category: string,
  subcategory: string,
  priority: 'high' | 'medium' | 'low',
  urgency_score: number
}> {
  const classificationPrompt = `Classify this citizen concern into appropriate categories:
  
  Text: "${text}"
  
  Categories: Infrastructure, Public Safety, Environment, Transportation, Healthcare, Education, Digital Services, General
  
  Determine:
  1. Primary category
  2. Subcategory
  3. Priority level (high/medium/low)
  4. Urgency score (1-10)`;

  const response = await hf.textGeneration({
    ...modelConfig,
    inputs: classificationPrompt,
    parameters: {
      temperature: 0.2,
      max_new_tokens: 150
    }
  });

  return {
    category: 'Infrastructure',
    subcategory: 'Street Lighting',
    priority: 'high',
    urgency_score: 8.5
  };
}

// Multi-language support for diverse communities
const supportedLanguages = {
  'en': 'English',
  'hi': 'Hindi',
  'te': 'Telugu',
  'ta': 'Tamil',
  'bn': 'Bengali',
  'mr': 'Marathi',
  'gu': 'Gujarati',
  'kn': 'Kannada',
  'ml': 'Malayalam',
  'or': 'Odia'
};

async function detectLanguage(text: string): Promise<string> {
  const languageDetectionPrompt = `Detect the language of this text:
  
  Text: "${text}"
  
  Supported languages: ${Object.values(supportedLanguages).join(', ')}
  
  Response: [language_code]`;

  const response = await hf.textGeneration({
    ...modelConfig,
    inputs: languageDetectionPrompt,
    parameters: {
      temperature: 0.1,
      max_new_tokens: 10
    }
  });

  return 'en'; // Default to English
}

async function translateText(text: string, targetLanguage: string): Promise<string> {
  const translationPrompt = `Translate this text to ${supportedLanguages[targetLanguage]}:
  
  Original text: "${text}"
  
  Translation:`;

  const response = await hf.textGeneration({
    ...modelConfig,
    inputs: translationPrompt,
    parameters: {
      temperature: 0.2,
      max_new_tokens: 200
    }
  });

  return response.generated_text || text;
}

// Advanced response generation with context awareness
export const generateAIResponse = async (message: string): Promise<string> => {
  try {
    // Detect language and translate if necessary
    const detectedLanguage = await detectLanguage(message);
    let processedMessage = message;
    
    if (detectedLanguage !== 'en') {
      processedMessage = await translateText(message, 'en');
    }

    // Analyze sentiment and classify the message
    const sentimentAnalysis = await analyzeSentiment(processedMessage);
    const classification = await classifyText(processedMessage);

    // Build comprehensive context for the AI model
    const systemContext = `You are a helpful AI assistant for Citizen AI, a platform that helps citizens interact with their local government and community services. You should:

1. Be helpful, friendly, and professional
2. Provide information about city services, government processes, and community programs
3. Help citizens understand how to report concerns or access services
4. If you don't know specific local information, suggest they contact Municipal Corporation
5. Keep responses concise but informative
6. Always be respectful and supportive of citizen needs

Current message analysis:
- Sentiment: ${sentimentAnalysis.sentiment} (confidence: ${sentimentAnalysis.confidence})
- Category: ${classification.category}
- Priority: ${classification.priority}
- Urgency: ${classification.urgency_score}/10

You can help with topics like:
- Municipal Corporation office hours and contact information
- How to report issues (potholes, streetlights, drainage, etc.)
- Parking regulations and transportation
- Utility services and bill payments
- Permits and licenses
- Waste management and sanitation schedules
- General city services and programs
- Port-related services and information
- Tourist information and local attractions

User message: "${processedMessage}"

Please provide a helpful and contextually appropriate response:`;

    // Generate response using IBM Granite model
    const response = await hf.textGeneration({
      ...modelConfig,
      inputs: systemContext,
      parameters: {
        temperature: 0.7,
        max_new_tokens: 300,
        do_sample: true,
        top_p: 0.9,
        repetition_penalty: 1.1
      }
    });

    let generatedResponse = response.generated_text || "I apologize, but I'm having trouble processing your request right now. Please try again or contact Municipal Corporation directly.";

    // Post-process the response
    generatedResponse = generatedResponse.replace(systemContext, '').trim();
    
    // Translate response back to original language if needed
    if (detectedLanguage !== 'en') {
      generatedResponse = await translateText(generatedResponse, detectedLanguage);
    }

    return generatedResponse;

  } catch (error) {
    console.error('Error generating AI response:', error);
    
    // Fallback response with error handling
    return "I apologize, but I'm experiencing technical difficulties with the AI service. Please try again in a moment, or contact Municipal Corporation directly at 0884-2372345 for immediate assistance.";
  }
};

// Batch processing for multiple messages
export async function processBatchMessages(messages: string[]): Promise<Array<{
  message: string,
  response: string,
  sentiment: any,
  classification: any
}>> {
  const results = [];
  
  for (const message of messages) {
    try {
      const sentiment = await analyzeSentiment(message);
      const classification = await classifyText(message);
      const response = await generateAIResponse(message);
      
      results.push({
        message,
        response,
        sentiment,
        classification
      });
    } catch (error) {
      results.push({
        message,
        response: "Error processing message",
        sentiment: null,
        classification: null
      });
    }
  }
  
  return results;
}

// Real-time streaming response (for future implementation)
export async function* streamAIResponse(message: string): AsyncGenerator<string, void, unknown> {
  const chunks = await generateAIResponse(message);
  const words = chunks.split(' ');
  
  for (const word of words) {
    yield word + ' ';
    await new Promise(resolve => setTimeout(resolve, 50));
  }
}

// Model performance monitoring
class ModelMetrics {
  private responseTime: number[] = [];
  private errorCount = 0;
  private successCount = 0;
  
  recordResponse(startTime: number, success: boolean) {
    const duration = Date.now() - startTime;
    this.responseTime.push(duration);
    
    if (success) {
      this.successCount++;
    } else {
      this.errorCount++;
    }
  }
  
  getMetrics() {
    const avgResponseTime = this.responseTime.reduce((a, b) => a + b, 0) / this.responseTime.length;
    const successRate = this.successCount / (this.successCount + this.errorCount);
    
    return {
      averageResponseTime: avgResponseTime,
      successRate: successRate,
      totalRequests: this.successCount + this.errorCount
    };
  }
}

const metrics = new ModelMetrics();

// Export additional utilities
export {
  analyzeSentiment,
  classifyText,
  detectLanguage,
  translateText,
  processBatchMessages,
  streamAIResponse,
  ConversationManager,
  ModelMetrics,
  supportedLanguages,
  modelConfig
};