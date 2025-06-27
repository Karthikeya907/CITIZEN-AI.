// Local AI service with predefined questions and answers for Kakinada City
export interface QAItem {
  id: string;
  question: string;
  answer: string;
  keywords: string[];
}

export const predefinedQA: QAItem[] = [
  // Casual conversation questions
  {
    id: 'casual1',
    question: 'Hi / Hello',
    answer: 'Hello! Welcome to Kakinada Citizen AI. I\'m here to help you with any questions about city services, community programs, or local government information in Kakinada. How can I assist you today?',
    keywords: ['hi', 'hello', 'hey', 'greetings', 'good morning', 'good afternoon', 'good evening', 'namaste']
  },
  {
    id: 'casual2',
    question: 'What about you?',
    answer: 'I\'m doing great, thank you for asking! I\'m here and ready to help you with any questions about Kakinada city services. I have information about municipal offices, permits, utilities, transportation, and much more. What would you like to know about our beautiful port city?',
    keywords: ['what about you', 'how are you', 'how are you doing', 'what about yourself']
  },
  {
    id: 'casual3',
    question: 'Can you assist me with city services?',
    answer: 'Absolutely! I\'d be happy to assist you with Kakinada city services. I can help you with information about municipal permits, utility bills, waste management, parking regulations, corporation meetings, reporting issues, and many other city services. What specific service are you interested in?',
    keywords: ['assist', 'help', 'city services', 'can you help', 'assistance', 'support', 'kakinada services']
  },
  {
    id: 'casual4',
    question: 'How are you doing?',
    answer: 'I\'m doing wonderful, thank you! I\'m here and ready to help you navigate Kakinada city services and answer your questions. Whether you need information about permits, utilities, or community programs in our port city, I\'m here to assist. What can I help you with today?',
    keywords: ['how are you doing', 'how are you', 'how do you do', 'how\'s it going']
  },
  {
    id: 'casual5',
    question: 'Thank you',
    answer: 'You\'re very welcome! I\'m glad I could help. If you have any other questions about Kakinada city services, community programs, or need assistance with anything else, please don\'t hesitate to ask. Have a great day in our beautiful port city!',
    keywords: ['thank you', 'thanks', 'thank you very much', 'appreciate it', 'grateful', 'dhanyawad']
  },
  {
    id: 'casual6',
    question: 'What can you help me with?',
    answer: 'I can help you with a wide range of Kakinada city services and information! Here are some areas I specialize in:\n\n• Municipal office hours and contact information\n• Reporting issues (street lights, potholes, drainage problems)\n• Utility services and bill payments\n• Permits and licenses (building, trade, vehicle permits)\n• Waste management and sanitation schedules\n• Parking regulations and transportation\n• Corporation meetings and civic participation\n• Community programs and welfare schemes\n• Port-related services and information\n• Tourist information and local attractions\n\nWhat specific topic about Kakinada interests you?',
    keywords: ['what can you help', 'what do you do', 'what services', 'what can you assist', 'capabilities']
  },
  {
    id: 'casual7',
    question: 'Good morning/afternoon/evening',
    answer: 'Good day to you too! I hope you\'re having a wonderful time in Kakinada. I\'m here to help you with any questions about city services, community programs, or local government information. How may I assist you today?',
    keywords: ['good morning', 'good afternoon', 'good evening', 'good day']
  },
  
  // City service questions (20 questions) - Kakinada name removed from questions
  {
    id: '1',
    question: 'What are the Municipal Corporation office hours?',
    answer: 'Kakinada Municipal Corporation office is open Monday through Friday from 10:00 AM to 5:00 PM, with a lunch break from 1:00 PM to 2:00 PM. Saturday hours are 10:00 AM to 2:00 PM. We are closed on Sundays and public holidays. For emergency services, please call 100 (Police) or 108 (Ambulance). The main office is located at Municipal Corporation Building, Main Road, Kakinada.',
    keywords: ['office', 'hours', 'open', 'closed', 'time', 'schedule', 'municipal corporation', 'kakinada corporation']
  },
  {
    id: '2',
    question: 'How do I report a street light that\'s out?',
    answer: 'You can report a broken or out street light by calling the Kakinada Municipal Corporation at 0884-2372345, or visit the Electrical Department at the Municipal Office. Please provide the exact location, nearest landmark, or ward number. Most street light repairs in Kakinada are completed within 5-7 business days. You can also report through the local ward member.',
    keywords: ['street light', 'streetlight', 'light', 'out', 'broken', 'report', 'repair', 'electrical']
  },
  {
    id: '3',
    question: 'When is waste collection in my area?',
    answer: 'Waste collection schedules in Kakinada vary by ward. Generally, residential areas have collection in the morning between 6:00 AM to 10:00 AM. To find your specific collection day and time, contact your local ward office or call the Sanitation Department at 0884-2372345. Please keep your waste ready before the collection vehicle arrives. Segregate wet and dry waste as per municipal guidelines.',
    keywords: ['waste', 'garbage', 'collection', 'pickup', 'schedule', 'sanitation', 'ward', 'segregation']
  },
  {
    id: '4',
    question: 'How do I get a building permit?',
    answer: 'To obtain a building permit in Kakinada, visit the Building Permission Department at Municipal Corporation or apply through AP Land Records website. You\'ll need to submit architectural plans, site survey, ownership documents, and pay the applicable fees. Processing time is typically 30-45 days for residential projects. For commercial projects, allow 60-90 days. Ensure compliance with Kakinada Development Authority guidelines.',
    keywords: ['building permit', 'permit', 'construction', 'building', 'renovation', 'plans', 'KDA', 'approval']
  },
  {
    id: '5',
    question: 'How can I pay my water bill?',
    answer: 'You can pay your Kakinada water bill online through AP Water Portal, at Municipal Corporation office, or at authorized collection centers. We accept cash, DD, and online payments. Bills are issued monthly and due within 15 days of issue. Late payment charges apply after the due date. For new connections or disconnections, visit the Water Works Department at Municipal Corporation.',
    keywords: ['water bill', 'pay', 'payment', 'utility', 'bill', 'online', 'due date', 'water works']
  },
  {
    id: '6',
    question: 'What are the parking regulations in city center?',
    answer: 'Parking in Kakinada city center (Main Road, Jagannaickpur, RTC Complex area) is regulated from 8 AM to 8 PM. Two-wheeler parking fee is ₹5 per day, four-wheeler is ₹10 per day. No parking zones are strictly enforced near hospitals, schools, and government offices. Violations result in ₹100 fine for two-wheelers and ₹200 for four-wheelers. Free parking is available at designated municipal parking areas.',
    keywords: ['parking', 'city center', 'main road', 'regulations', 'fine', 'fee', 'vehicle']
  },
  {
    id: '7',
    question: 'How do I register to vote?',
    answer: 'You can register to vote in Kakinada at the Electoral Registration Office, Collectorate, or online through the National Voters\' Service Portal (NVSP). You must be 18 years old, an Indian citizen, and a resident of Kakinada. Bring Aadhaar card, address proof, and passport-size photo. Registration is ongoing, but there are specific deadlines before each election. Contact the District Election Officer for assistance.',
    keywords: ['vote', 'register', 'voting', 'election', 'registration', 'NVSP', 'electoral', 'collectorate']
  },
  {
    id: '8',
    question: 'When are Municipal Corporation council meetings held?',
    answer: 'Kakinada Municipal Corporation council meetings are typically held on the last Friday of each month at 11:00 AM in the Corporation Council Hall. Special meetings may be called as needed. Meetings are open to the public, and there\'s a public grievance session. Meeting agendas are displayed on the notice board 48 hours in advance. Citizens can submit petitions through their ward corporators.',
    keywords: ['municipal corporation', 'council', 'meeting', 'corporator', 'public', 'agenda', 'grievance']
  },
  {
    id: '9',
    question: 'How do I report a pothole or road damage?',
    answer: 'Report potholes and road damage by calling the Engineering Department at 0884-2372345 or visiting the Municipal Corporation office. Provide the exact location, road name, and severity of damage. For major roads (NH-16, SH-41), contact the respective highway authorities. Emergency repairs on main roads are addressed within 48 hours, while internal roads may take 7-10 days depending on monsoon season.',
    keywords: ['pothole', 'road', 'damage', 'repair', 'report', 'engineering', 'highway', 'NH-16']
  },
  {
    id: '10',
    question: 'What waste management and recycling programs are available?',
    answer: 'Kakinada follows segregated waste collection - green bins for wet waste, blue bins for dry waste. Plastic waste is collected separately on designated days. The city has a composting facility at Turangi. E-waste collection drives are conducted quarterly. Hazardous waste should be disposed of at the designated facility near Industrial Estate. Contact Sanitation Department for bulk waste disposal arrangements.',
    keywords: ['waste management', 'recycling', 'segregation', 'composting', 'e-waste', 'hazardous', 'sanitation']
  },
  {
    id: '11',
    question: 'How do I get a trade license?',
    answer: 'Trade licenses in Kakinada can be obtained from the Revenue Department at Municipal Corporation. You\'ll need to provide business details, property documents, NOC from Fire Department (if required), and pay the license fee (₹500-₹5000 depending on business type). Processing takes 15-30 days. Renewal is required annually. Some businesses may need additional clearances from Pollution Control Board.',
    keywords: ['trade license', 'business license', 'license', 'business', 'revenue', 'NOC', 'renewal']
  },
  {
    id: '12',
    question: 'What are the noise pollution rules?',
    answer: 'Kakinada follows Andhra Pradesh Pollution Control Board noise regulations. Silence zones (near hospitals, schools, courts) have 50 dB day/40 dB night limits. Residential areas: 55 dB day/45 dB night. Commercial areas: 65 dB day/55 dB night. Loudspeakers require police permission and must stop by 10 PM. Report noise complaints to local police station or call 100.',
    keywords: ['noise pollution', 'noise', 'complaint', 'loudspeaker', 'silence zone', 'decibel', 'APPCB']
  },
  {
    id: '13',
    question: 'How do I report water supply issues?',
    answer: 'Report water supply issues, leakages, or contamination to the Water Works Department at 0884-2372345. For emergency water supply disruptions, call the 24-hour helpline. Kakinada gets water supply from Godavari river and local bore wells. Supply timings vary by area - typically morning 6-8 AM and evening 6-8 PM. Water tanker services are available during shortages.',
    keywords: ['water supply', 'water problem', 'leakage', 'contamination', 'godavari', 'tanker', 'bore well']
  },
  {
    id: '14',
    question: 'When are property taxes due?',
    answer: 'Property taxes in Kakinada are due annually by March 31st. You can pay online through AP Land Records portal, at Municipal Corporation office, or at designated banks. Early payment (before December 31st) gets 5% discount. Penalty of 2% per month applies for late payments. Property tax is calculated based on Annual Rental Value (ARV) and property classification.',
    keywords: ['property tax', 'taxes', 'due', 'payment', 'penalty', 'discount', 'ARV', 'annual']
  },
  {
    id: '15',
    question: 'How do I arrange bulk waste disposal?',
    answer: 'For bulk waste disposal in Kakinada (furniture, construction debris, large appliances), contact the Sanitation Department at least 2 days in advance. There\'s a fee of ₹200-₹500 depending on quantity. Construction waste should be disposed at the designated site near Turangi. Electronic waste can be given to authorized e-waste collectors. Hazardous materials require special handling.',
    keywords: ['bulk waste', 'disposal', 'construction debris', 'furniture', 'appliances', 'e-waste', 'hazardous']
  },
  {
    id: '16',
    question: 'What public transportation options are available?',
    answer: 'Kakinada has APSRTC bus services connecting to major destinations. Local transportation includes auto-rickshaws (₹15 minimum fare), city buses, and private buses. The main bus station is at RTC Complex. Railway connectivity is through Kakinada Town and Kakinada Port stations. For airport, the nearest is Rajahmundry (60 km). App-based cabs and bike taxis are also available.',
    keywords: ['public transportation', 'bus', 'APSRTC', 'auto', 'railway', 'RTC complex', 'transport']
  },
  {
    id: '17',
    question: 'How do I report illegal dumping or littering?',
    answer: 'Report illegal dumping, littering, or unauthorized waste disposal to the Sanitation Department at 0884-2372345 or to the local police station. Fines for littering range from ₹100-₹500. Take photos if possible and provide exact location. The city has installed CCTV cameras in several areas to monitor illegal dumping. Repeat offenders face higher penalties.',
    keywords: ['illegal dumping', 'littering', 'waste disposal', 'fine', 'CCTV', 'unauthorized', 'penalty']
  },
  {
    id: '18',
    question: 'What welfare schemes and community programs are available for senior citizens?',
    answer: 'Kakinada offers several programs for senior citizens: Pension schemes (Old Age Pension ₹3000/month), free health checkups at government hospitals, senior citizen cards for discounts, and recreational activities at community centers. The District Social Welfare Office provides information on central and state schemes. Regular health camps are organized in various wards.',
    keywords: ['senior citizens', 'elderly', 'pension', 'welfare schemes', 'health checkup', 'community programs', 'social welfare']
  },
  {
    id: '19',
    question: 'How do I register my vehicle?',
    answer: 'Vehicle registration in Kakinada is done at the Regional Transport Office (RTO) located at Surya Rao Pet. You need insurance, pollution certificate, dealer invoice, and identity documents. Online slot booking is available through AP Transport website. Registration fees vary by vehicle type. Temporary registration is valid for 1 month. Permanent registration takes 7-15 days.',
    keywords: ['vehicle registration', 'RTO', 'transport office', 'registration fee', 'insurance', 'pollution certificate']
  },
  {
    id: '20',
    question: 'What are the library and educational facilities available?',
    answer: 'Kakinada has several libraries: District Central Library (Jagannaickpur), Municipal Library (Main Road), and college libraries. Timings are generally 9 AM to 8 PM. Educational institutions include JNTU Kakinada, Government Degree Colleges, and numerous schools. Free WiFi is available at public libraries. Digital literacy programs are conducted for citizens. Library membership is free for students and nominal fee for others.',
    keywords: ['library', 'education', 'JNTU', 'books', 'digital literacy', 'WiFi', 'membership', 'college']
  }
];

export const generateAIResponse = async (message: string): Promise<string> => {
  // Simulate API delay for realistic experience
  await new Promise(resolve => setTimeout(resolve, 1000));

  const userMessage = message.toLowerCase().trim();
  
  // Find the best matching Q&A based on keywords
  let bestMatch: QAItem | null = null;
  let highestScore = 0;

  for (const qa of predefinedQA) {
    let score = 0;
    
    // Check for exact question match first
    if (qa.question.toLowerCase() === userMessage) {
      return qa.answer;
    }
    
    // Check keywords
    for (const keyword of qa.keywords) {
      if (userMessage.includes(keyword.toLowerCase())) {
        score += keyword.length; // Longer keywords get higher weight
      }
    }
    
    if (score > highestScore) {
      highestScore = score;
      bestMatch = qa;
    }
  }

  // If we found a good match (score > 3), return the answer
  if (bestMatch && highestScore > 3) {
    return bestMatch.answer;
  }

  // Default response for unmatched queries with Kakinada-specific information
  return `I understand you're asking about "${message}". While I don't have a specific answer for that question, I can help you with common Kakinada city services and information. Here are some topics I can assist with:

• Municipal Corporation office hours and contact information
• Reporting issues (street lights, potholes, drainage, etc.)
• Utility services and bill payments
• Permits and licenses (building, trade, vehicle registration)
• Waste management and sanitation schedules
• Parking regulations and transportation
• Corporation council meetings and civic participation
• Community programs and welfare schemes
• Port-related services and information
• Educational facilities and libraries

Please try asking about one of these topics, or contact Kakinada Municipal Corporation directly at 0884-2372345 for personalized assistance.`;
};

export const getRandomQuestions = (count: number = 5): QAItem[] => {
  // Filter out casual questions for quick actions, show only city service questions
  const cityServiceQuestions = predefinedQA.filter(qa => !qa.id.startsWith('casual'));
  const shuffled = [...cityServiceQuestions].sort(() => 0.5 - Math.random());
  return shuffled.slice(0, count);
};