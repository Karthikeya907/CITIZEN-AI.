import React, { createContext, useContext, useState, ReactNode } from 'react';

export interface Concern {
  id: string;
  message: string;
  sentiment: 'positive' | 'negative' | 'neutral';
  timestamp: string;
  category: string;
  type: 'concern' | 'feedback';
  priority: 'high' | 'medium' | 'low';
}

interface DataContextType {
  concerns: Concern[];
  addConcern: (concern: Omit<Concern, 'id' | 'timestamp' | 'priority'>) => void;
  getConcernsByType: (type: 'concern' | 'feedback') => Concern[];
}

const DataContext = createContext<DataContextType | undefined>(undefined);

export const useData = () => {
  const context = useContext(DataContext);
  if (context === undefined) {
    throw new Error('useData must be used within a DataProvider');
  }
  return context;
};

interface DataProviderProps {
  children: ReactNode;
}

export const DataProvider: React.FC<DataProviderProps> = ({ children }) => {
  const [concerns, setConcerns] = useState<Concern[]>([
    {
      id: '1',
      message: "The streetlight near Kakinada Port area has been out for a week, causing safety concerns for night workers",
      category: "Infrastructure",
      sentiment: "negative",
      timestamp: new Date(Date.now() - 2 * 60 * 60 * 1000).toLocaleString(),
      type: "concern",
      priority: "high"
    },
    {
      id: '3',
      message: "Great job on the new community center at Jagannaickpur! The facilities are excellent and well-maintained",
      category: "General",
      sentiment: "positive",
      timestamp: new Date(Date.now() - 4 * 60 * 60 * 1000).toLocaleString(),
      type: "feedback",
      priority: "low"
    },
    {
      id: '5',
      message: "Need more police patrols in the evening hours around Main Road market area for better security",
      category: "Public Safety",
      sentiment: "neutral",
      timestamp: new Date(Date.now() - 6 * 60 * 60 * 1000).toLocaleString(),
      type: "concern",
      priority: "medium"
    },
    {
      id: '7',
      message: "The new waste segregation program in Kakinada is working well, streets are much cleaner now",
      category: "Environment",
      sentiment: "positive",
      timestamp: new Date(Date.now() - 8 * 60 * 60 * 1000).toLocaleString(),
      type: "feedback",
      priority: "low"
    },
    {
      id: '9',
      message: "APSRTC bus route to Industrial Estate is frequently delayed, affecting daily commuters",
      category: "Transportation",
      sentiment: "negative",
      timestamp: new Date(Date.now() - 12 * 60 * 60 * 1000).toLocaleString(),
      type: "concern",
      priority: "medium"
    },
    {
      id: '11',
      message: "Water supply timing in Suryarao Pet area is irregular, sometimes no water for 2-3 days",
      category: "Infrastructure",
      sentiment: "negative",
      timestamp: new Date(Date.now() - 14 * 60 * 60 * 1000).toLocaleString(),
      type: "concern",
      priority: "high"
    },
    {
      id: '13',
      message: "The digital library services at District Central Library are very helpful for students",
      category: "Education",
      sentiment: "positive",
      timestamp: new Date(Date.now() - 16 * 60 * 60 * 1000).toLocaleString(),
      type: "feedback",
      priority: "low"
    },
    {
      id: '15',
      message: "Drainage system near RTC Complex gets clogged during monsoon, causing waterlogging",
      category: "Infrastructure",
      sentiment: "negative",
      timestamp: new Date(Date.now() - 18 * 60 * 60 * 1000).toLocaleString(),
      type: "concern",
      priority: "high"
    },
    {
      id: '17',
      message: "Appreciate the senior citizen health camps organized by Municipal Corporation, very beneficial",
      category: "Healthcare",
      sentiment: "positive",
      timestamp: new Date(Date.now() - 20 * 60 * 60 * 1000).toLocaleString(),
      type: "feedback",
      priority: "low"
    },
    {
      id: '19',
      message: "Parking fees at Main Road are reasonable and the system is well-organized",
      category: "Transportation",
      sentiment: "positive",
      timestamp: new Date(Date.now() - 22 * 60 * 60 * 1000).toLocaleString(),
      type: "feedback",
      priority: "low"
    },
    {
      id: '21',
      message: "Road conditions on the way to JNTU Kakinada campus need immediate repair, many potholes",
      category: "Infrastructure",
      sentiment: "negative",
      timestamp: new Date(Date.now() - 24 * 60 * 60 * 1000).toLocaleString(),
      type: "concern",
      priority: "medium"
    },
    {
      id: '23',
      message: "The online property tax payment system is user-friendly and saves a lot of time",
      category: "Digital Services",
      sentiment: "positive",
      timestamp: new Date(Date.now() - 26 * 60 * 60 * 1000).toLocaleString(),
      type: "feedback",
      priority: "low"
    },
    {
      id: '25',
      message: "Illegal dumping of construction waste near Turangi area is increasing, needs attention",
      category: "Environment",
      sentiment: "negative",
      timestamp: new Date(Date.now() - 28 * 60 * 60 * 1000).toLocaleString(),
      type: "concern",
      priority: "medium"
    },
    {
      id: '27',
      message: "The new LED street lights installed in residential areas are much brighter and energy-efficient",
      category: "Infrastructure",
      sentiment: "positive",
      timestamp: new Date(Date.now() - 30 * 60 * 60 * 1000).toLocaleString(),
      type: "feedback",
      priority: "low"
    },
    {
      id: '29',
      message: "Auto-rickshaw drivers near railway station are not using meters, overcharging passengers",
      category: "Transportation",
      sentiment: "negative",
      timestamp: new Date(Date.now() - 32 * 60 * 60 * 1000).toLocaleString(),
      type: "concern",
      priority: "medium"
    },
    {
      id: '31',
      message: "Municipal Corporation's response to citizen complaints has improved significantly this year",
      category: "General",
      sentiment: "positive",
      timestamp: new Date(Date.now() - 34 * 60 * 60 * 1000).toLocaleString(),
      type: "feedback",
      priority: "low"
    },
    {
      id: '33',
      message: "Need better traffic management during festival seasons, especially near temples",
      category: "Transportation",
      sentiment: "neutral",
      timestamp: new Date(Date.now() - 36 * 60 * 60 * 1000).toLocaleString(),
      type: "concern",
      priority: "medium"
    },
    {
      id: '35',
      message: "The beach cleaning drive organized by the city was excellent, great community participation",
      category: "Environment",
      sentiment: "positive",
      timestamp: new Date(Date.now() - 38 * 60 * 60 * 1000).toLocaleString(),
      type: "feedback",
      priority: "low"
    },
    {
      id: '37',
      message: "Power cuts in Industrial Estate area are affecting business operations, need stable supply",
      category: "Infrastructure",
      sentiment: "negative",
      timestamp: new Date(Date.now() - 40 * 60 * 60 * 1000).toLocaleString(),
      type: "concern",
      priority: "high"
    },
    {
      id: '39',
      message: "The new mobile app for municipal services is very convenient for bill payments and complaints",
      category: "Digital Services",
      sentiment: "positive",
      timestamp: new Date(Date.now() - 42 * 60 * 60 * 1000).toLocaleString(),
      type: "feedback",
      priority: "low"
    },
    {
      id: '41',
      message: "Stray dogs in residential areas are becoming a safety concern, especially for children",
      category: "Public Safety",
      sentiment: "negative",
      timestamp: new Date(Date.now() - 44 * 60 * 60 * 1000).toLocaleString(),
      type: "concern",
      priority: "high"
    },
    {
      id: '43',
      message: "The new playground equipment at Central Park is fantastic, kids love it",
      category: "Recreation",
      sentiment: "positive",
      timestamp: new Date(Date.now() - 46 * 60 * 60 * 1000).toLocaleString(),
      type: "feedback",
      priority: "low"
    },
    {
      id: '45',
      message: "Public toilets near bus stand are not properly maintained, need regular cleaning",
      category: "Sanitation",
      sentiment: "negative",
      timestamp: new Date(Date.now() - 48 * 60 * 60 * 1000).toLocaleString(),
      type: "concern",
      priority: "medium"
    },
    {
      id: '47',
      message: "The free WiFi service at public libraries is working great, very helpful for students",
      category: "Digital Services",
      sentiment: "positive",
      timestamp: new Date(Date.now() - 50 * 60 * 60 * 1000).toLocaleString(),
      type: "feedback",
      priority: "low"
    },
    {
      id: '49',
      message: "Traffic signals at major intersections are not synchronized, causing unnecessary delays",
      category: "Transportation",
      sentiment: "negative",
      timestamp: new Date(Date.now() - 52 * 60 * 60 * 1000).toLocaleString(),
      type: "concern",
      priority: "medium"
    },
    {
      id: '51',
      message: "The vaccination drive organized by health department was very well managed",
      category: "Healthcare",
      sentiment: "positive",
      timestamp: new Date(Date.now() - 54 * 60 * 60 * 1000).toLocaleString(),
      type: "feedback",
      priority: "low"
    },
    {
      id: '53',
      message: "Mosquito breeding in stagnant water near residential areas needs immediate attention",
      category: "Public Health",
      sentiment: "negative",
      timestamp: new Date(Date.now() - 56 * 60 * 60 * 1000).toLocaleString(),
      type: "concern",
      priority: "high"
    },
    {
      id: '55',
      message: "The cultural events organized during festivals bring the community together beautifully",
      category: "Culture",
      sentiment: "positive",
      timestamp: new Date(Date.now() - 58 * 60 * 60 * 1000).toLocaleString(),
      type: "feedback",
      priority: "low"
    },
    {
      id: '57',
      message: "Street vendors are blocking footpaths, making it difficult for pedestrians to walk",
      category: "Public Safety",
      sentiment: "negative",
      timestamp: new Date(Date.now() - 60 * 60 * 60 * 1000).toLocaleString(),
      type: "concern",
      priority: "medium"
    },
    {
      id: '59',
      message: "The new bus shelters with seating arrangements are a great addition to the city",
      category: "Transportation",
      sentiment: "positive",
      timestamp: new Date(Date.now() - 62 * 60 * 60 * 1000).toLocaleString(),
      type: "feedback",
      priority: "low"
    },
    {
      id: '61',
      message: "Unauthorized construction activities are happening without proper permits in several areas",
      category: "Urban Planning",
      sentiment: "negative",
      timestamp: new Date(Date.now() - 64 * 60 * 60 * 1000).toLocaleString(),
      type: "concern",
      priority: "high"
    },
    {
      id: '63',
      message: "The tree plantation drive has made the city greener and more beautiful",
      category: "Environment",
      sentiment: "positive",
      timestamp: new Date(Date.now() - 66 * 60 * 60 * 1000).toLocaleString(),
      type: "feedback",
      priority: "low"
    },
    {
      id: '65',
      message: "Water logging during heavy rains is a recurring problem in low-lying areas",
      category: "Infrastructure",
      sentiment: "negative",
      timestamp: new Date(Date.now() - 68 * 60 * 60 * 1000).toLocaleString(),
      type: "concern",
      priority: "high"
    },
    {
      id: '67',
      message: "The skill development programs for youth are providing excellent training opportunities",
      category: "Education",
      sentiment: "positive",
      timestamp: new Date(Date.now() - 70 * 60 * 60 * 1000).toLocaleString(),
      type: "feedback",
      priority: "low"
    },
    {
      id: '69',
      message: "Illegal parking of heavy vehicles on residential roads is causing traffic congestion",
      category: "Transportation",
      sentiment: "negative",
      timestamp: new Date(Date.now() - 72 * 60 * 60 * 1000).toLocaleString(),
      type: "concern",
      priority: "medium"
    },
    {
      id: '71',
      message: "The women's safety initiatives and helpline services are very reassuring",
      category: "Public Safety",
      sentiment: "positive",
      timestamp: new Date(Date.now() - 74 * 60 * 60 * 1000).toLocaleString(),
      type: "feedback",
      priority: "low"
    },
    {
      id: '73',
      message: "Air pollution levels are increasing due to industrial emissions, need monitoring",
      category: "Environment",
      sentiment: "negative",
      timestamp: new Date(Date.now() - 76 * 60 * 60 * 1000).toLocaleString(),
      type: "concern",
      priority: "high"
    },
    {
      id: '75',
      message: "The sports facilities at the stadium are well-maintained and accessible to all",
      category: "Recreation",
      sentiment: "positive",
      timestamp: new Date(Date.now() - 78 * 60 * 60 * 1000).toLocaleString(),
      type: "feedback",
      priority: "low"
    },
    {
      id: '77',
      message: "Frequent power outages during summer months are affecting daily life and businesses",
      category: "Infrastructure",
      sentiment: "negative",
      timestamp: new Date(Date.now() - 80 * 60 * 60 * 1000).toLocaleString(),
      type: "concern",
      priority: "high"
    },
    {
      id: '79',
      message: "The disaster management preparedness and response system has improved significantly",
      category: "Emergency Services",
      sentiment: "positive",
      timestamp: new Date(Date.now() - 82 * 60 * 60 * 1000).toLocaleString(),
      type: "feedback",
      priority: "low"
    },
    {
      id: '81',
      message: "Inadequate lighting in parks makes them unsafe for evening walks and exercise",
      category: "Public Safety",
      sentiment: "negative",
      timestamp: new Date(Date.now() - 84 * 60 * 60 * 1000).toLocaleString(),
      type: "concern",
      priority: "medium"
    },
    {
      id: '83',
      message: "The citizen grievance redressal system is now more transparent and efficient",
      category: "General",
      sentiment: "positive",
      timestamp: new Date(Date.now() - 86 * 60 * 60 * 1000).toLocaleString(),
      type: "feedback",
      priority: "low"
    },
    {
      id: '85',
      message: "Road maintenance work is causing severe traffic jams during peak hours",
      category: "Transportation",
      sentiment: "negative",
      timestamp: new Date(Date.now() - 88 * 60 * 60 * 1000).toLocaleString(),
      type: "concern",
      priority: "medium"
    },
    {
      id: '87',
      message: "The community health centers are providing quality healthcare services to residents",
      category: "Healthcare",
      sentiment: "positive",
      timestamp: new Date(Date.now() - 90 * 60 * 60 * 1000).toLocaleString(),
      type: "feedback",
      priority: "low"
    },
    {
      id: '89',
      message: "Encroachment of public spaces by private parties needs immediate action",
      category: "Urban Planning",
      sentiment: "negative",
      timestamp: new Date(Date.now() - 92 * 60 * 60 * 1000).toLocaleString(),
      type: "concern",
      priority: "high"
    },
    {
      id: '91',
      message: "The digital governance initiatives have made government services more accessible",
      category: "Digital Services",
      sentiment: "positive",
      timestamp: new Date(Date.now() - 94 * 60 * 60 * 1000).toLocaleString(),
      type: "feedback",
      priority: "low"
    },
    {
      id: '93',
      message: "Lack of proper signage and directions is confusing for visitors and new residents",
      category: "Infrastructure",
      sentiment: "negative",
      timestamp: new Date(Date.now() - 96 * 60 * 60 * 1000).toLocaleString(),
      type: "concern",
      priority: "medium"
    },
    {
      id: '95',
      message: "The environmental awareness campaigns are educating people about sustainable living",
      category: "Environment",
      sentiment: "positive",
      timestamp: new Date(Date.now() - 98 * 60 * 60 * 1000).toLocaleString(),
      type: "feedback",
      priority: "low"
    },
    {
      id: '97',
      message: "Public transport frequency is insufficient during peak hours, causing overcrowding",
      category: "Transportation",
      sentiment: "negative",
      timestamp: new Date(Date.now() - 100 * 60 * 60 * 1000).toLocaleString(),
      type: "concern",
      priority: "medium"
    },
    {
      id: '99',
      message: "The financial assistance programs for small businesses are helping local entrepreneurs",
      category: "Economic Development",
      sentiment: "positive",
      timestamp: new Date(Date.now() - 102 * 60 * 60 * 1000).toLocaleString(),
      type: "feedback",
      priority: "low"
    }
  ]);

  const determinePriority = (sentiment: string, category: string): 'high' | 'medium' | 'low' => {
    if (sentiment === 'negative') {
      if (category === 'Public Safety' || category === 'Infrastructure') {
        return 'high';
      }
      return 'medium';
    }
    if (sentiment === 'neutral') {
      return 'medium';
    }
    return 'low';
  };

  const addConcern = (concernData: Omit<Concern, 'id' | 'timestamp' | 'priority'>) => {
    const newConcern: Concern = {
      ...concernData,
      id: Date.now().toString(),
      timestamp: new Date().toLocaleString(),
      priority: determinePriority(concernData.sentiment, concernData.category)
    };
    
    setConcerns(prev => [newConcern, ...prev]);
  };

  const getConcernsByType = (type: 'concern' | 'feedback') => {
    return concerns.filter(concern => concern.type === type);
  };

  return (
    <DataContext.Provider value={{ concerns, addConcern, getConcernsByType }}>
      {children}
    </DataContext.Provider>
  );
};