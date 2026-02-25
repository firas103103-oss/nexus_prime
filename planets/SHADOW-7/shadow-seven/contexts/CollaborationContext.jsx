import React, { createContext, useContext, useState, useCallback } from 'react';

/**
 * Collaboration Context — Local mode (no Supabase Realtime)
 * Provides no-op implementations for collaboration features.
 */
const CollaborationContext = createContext();

export const useCollaboration = () => {
  const context = useContext(CollaborationContext);
  if (!context) {
    throw new Error('useCollaboration must be used within CollaborationProvider');
  }
  return context;
};

export const CollaborationProvider = ({ children }) => {
  const [activeUsers, setActiveUsers] = useState([]);
  const [currentDocument, setCurrentDocument] = useState(null);
  const [changes, setChanges] = useState([]);

  const initCollaboration = useCallback(async (documentId, userId) => {
    setCurrentDocument(documentId);
    setActiveUsers([{ userId, timestamp: new Date().toISOString() }]);
    return null;
  }, []);

  const endCollaboration = useCallback(async () => {
    setCurrentDocument(null);
    setActiveUsers([]);
    setChanges([]);
  }, []);

  const broadcastChange = useCallback(async () => {}, []);
  const broadcastCursor = useCallback(async () => {}, []);

  const value = {
    activeUsers,
    currentDocument,
    changes,
    initCollaboration,
    endCollaboration,
    broadcastChange,
    broadcastCursor
  };

  return (
    <CollaborationContext.Provider value={value}>
      {children}
    </CollaborationContext.Provider>
  );
};

export default CollaborationProvider;
