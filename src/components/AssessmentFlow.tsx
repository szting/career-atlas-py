import React, { useState } from 'react';
import { PersonaSelection } from './PersonaSelection';
import { WelcomeScreen } from './WelcomeScreen';
import { RIASECAssessment } from './RIASECAssessment';
import { SkillsAssessment } from './SkillsAssessment';
import { WorkValuesAssessment } from './WorkValuesAssessment';
import { PersonaType, UserProfile, RIASECScore } from '../types';

interface AssessmentFlowProps {
  onComplete: (profile: UserProfile) => void;
}

type AssessmentStep = 'persona' | 'welcome' | 'riasec' | 'skills' | 'values';

export const AssessmentFlow: React.FC<AssessmentFlowProps> = ({ onComplete }) => {
  const [currentStep, setCurrentStep] = useState<AssessmentStep>('persona');
  const [selectedPersona, setSelectedPersona] = useState<PersonaType | null>(null);
  const [userName, setUserName] = useState<string>('');
  const [riasecScores, setRiasecScores] = useState<RIASECScore | null>(null);
  const [skillsData, setSkillsData] = useState<{ [key: string]: number } | null>(null);

  const handlePersonaSelect = (persona: PersonaType) => {
    setSelectedPersona(persona);
    setCurrentStep('welcome');
  };

  const handleNameSubmit = (name: string) => {
    setUserName(name);
    setCurrentStep('riasec');
  };

  const handleRIASECComplete = (scores: RIASECScore) => {
    setRiasecScores(scores);
    setCurrentStep('skills');
  };

  const handleSkillsComplete = (skills: { [key: string]: number }) => {
    setSkillsData(skills);
    setCurrentStep('values');
  };

  const handleValuesComplete = (values: string[]) => {
    if (selectedPersona && riasecScores && skillsData) {
      const userProfile: UserProfile = {
        persona: selectedPersona,
        name: userName,
        riasecScores,
        skills: skillsData,
        workValues: values,
        completedAt: new Date().toISOString()
      };
      onComplete(userProfile);
    }
  };

  const handleStepBack = () => {
    switch (currentStep) {
      case 'welcome':
        setCurrentStep('persona');
        break;
      case 'riasec':
        setCurrentStep('welcome');
        break;
      case 'skills':
        setCurrentStep('riasec');
        break;
      case 'values':
        setCurrentStep('skills');
        break;
    }
  };

  switch (currentStep) {
    case 'persona':
      return <PersonaSelection onPersonaSelect={handlePersonaSelect} />;
    case 'welcome':
      return selectedPersona ? (
        <WelcomeScreen 
          onNameSubmit={handleNameSubmit} 
          selectedPersona={selectedPersona} 
        />
      ) : (
        <PersonaSelection onPersonaSelect={handlePersonaSelect} />
      );
    case 'riasec':
      return <RIASECAssessment onComplete={handleRIASECComplete} onBack={() => handleStepBack()} />;
    case 'skills':
      return <SkillsAssessment onComplete={handleSkillsComplete} onBack={() => handleStepBack()} />;
    case 'values':
      return <WorkValuesAssessment onComplete={handleValuesComplete} onBack={() => handleStepBack()} />;
    default:
      return <PersonaSelection onPersonaSelect={handlePersonaSelect} />;
  }
};
