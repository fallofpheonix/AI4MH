export interface SyndromeAnalysis {
  name: string;
  description: string;
  example: string;
  difficulty: 'easy' | 'medium' | 'hard';
}

export function analyzeCommunity(community: string): SyndromeAnalysis {
  const analyses: Record<string, SyndromeAnalysis> = {
    'Cinema Forum': {
      name: 'The Nostalgia Filter',
      description: 'Users consistently rate older movies higher than new ones, regardless of actual quality.',
      example: '"They don\'t make movies like they used to in the 90s"',
      difficulty: 'easy'
    },
    'Tech Circle': {
      name: 'The Hype Cycle Trap',
      description: 'Technology is either world-changing or useless, with no middle ground.',
      example: '"This AI will either solve all problems or destroy humanity"',
      difficulty: 'medium'
    }
  };

  return analyses[community] || {
    name: 'General Groupthink',
    description: 'The community reinforces popular opinions and suppresses minority viewpoints.',
    example: 'Downvoting contrary opinions without engagement',
    difficulty: 'medium'
  };
}

export function evaluateIntervention(intervention: string, syndrome: string): { success: boolean; feedback: string } {
  const interventionLower = intervention.toLowerCase();
  
  if (interventionLower.includes('question') || interventionLower.includes('why')) {
    return {
      success: true,
      feedback: 'Excellent! Asking probing questions helps break the thought pattern.'
    };
  }

  if (interventionLower.includes('evidence') || interventionLower.includes('research')) {
    return {
      success: true, 
      feedback: 'Great use of evidence to challenge the assumption.'
    };
  }

  const success = Math.random() > 0.3;
  
  return {
    success,
    feedback: success 
      ? 'Your perspective successfully challenged the groupthink!'
      : 'The community dismissed your argument. Try a different approach.'
  };
}
