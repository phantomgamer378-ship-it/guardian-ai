# Guardian AI - React Frontend Setup

## Project Structure
```
guardian-ai-frontend/
├── components/
│   └── ui/
│       └── animated-ai-chat.tsx
├── lib/
│   └── utils.ts
├── app/
│   ├── globals.css
│   ├── layout.tsx
│   └── page.tsx
├── package.json
└── next.config.js
```

## Setup Instructions

### 1. Initialize Next.js with TypeScript
```bash
npx create-next-app@latest guardian-ai-frontend --typescript --tailwind --eslint
cd guardian-ai-frontend
```

### 2. Install Dependencies
```bash
npm install lucide-react framer-motion
npm install -D @types/node
```

### 3. Configure Tailwind
```css
/* app/globals.css */
@tailwind base;
@tailwind components;
@tailwind utilities;

.lab-bg::before {
  overflow: hidden;
  max-width: 100vw;
  max-height: 100vh;
  box-sizing: border-box;
}

:root {
  --background: #0a0a0a;
  --foreground: #ffffff;
}

body {
  background: var(--background);
  color: var(--foreground);
}
```

### 4. Create Utility Function
```typescript
// lib/utils.ts
import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
```

### 5. Create Main Component
Copy the animated-ai-chat.tsx to components/ui/

### 6. Integrate with Guardian AI API
Replace the component with this integrated version:

```tsx
// components/ui/animated-ai-chat.tsx
"use client";

import { useEffect, useRef, useCallback, useTransition, useState } from "react";
import { cn } from "@/lib/utils";
import {
    SendIcon,
    Paperclip,
    PlusIcon,
    XIcon,
    LoaderIcon,
} from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import * as React from "react"

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1/chat';

interface TextareaProps extends React.TextareaHTMLAttributes<HTMLTextAreaElement> {
  containerClassName?: string;
  showRing?: boolean;
}

const Textarea = React.forwardRef<HTMLTextAreaElement, TextareaProps>(
  ({ className, containerClassName, showRing = true, ...props }, ref) => {
    const [isFocused, setIsFocused] = React.useState(false);
    
    return (
      <div className={cn("relative", containerClassName)}>
        <textarea
          className={cn(
            "flex min-h-[80px] w-full rounded-md border border-input bg-background px-3 py-2 text-sm",
            "transition-all duration-200 ease-in-out",
            "placeholder:text-muted-foreground",
            "disabled:cursor-not-allowed disabled:opacity-50",
            showRing ? "focus-visible:outline-none focus-visible:ring-0 focus-visible:ring-offset-0" : "",
            className
          )}
          ref={ref}
          onFocus={() => setIsFocused(true)}
          onBlur={() => setIsFocused(false)}
          {...props}
        />
        
        {showRing && isFocused && (
          <motion.span 
            className="absolute inset-0 rounded-md pointer-events-none ring-2 ring-offset-0 ring-violet-500/30"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.2 }}
          />
        )}
      </div>
    )
  }
)
Textarea.displayName = "Textarea"

interface Message {
  text: string;
  sender: 'user' | 'bot';
  timestamp: Date;
}

export function AnimatedAIChat() {
    const [value, setValue] = useState("");
    const [messages, setMessages] = useState<Message[]>([]);
    const [isTyping, setIsTyping] = useState(false);
    const [isPending, startTransition] = useTransition();
    const [attachments, setAttachments] = useState<string[]>([]);
    
    const textareaRef = useRef<HTMLTextAreaElement>(null);
    const chatContainerRef = useRef<HTMLDivElement>(null);

    const adjustHeight = useCallback((reset?: boolean) => {
        const textarea = textareaRef.current;
        if (!textarea) return;

        if (reset) {
            textarea.style.height = "80px";
            return;
        }

        textarea.style.height = "80px";
        const newHeight = Math.max(80, Math.min(textarea.scrollHeight, 200));
        textarea.style.height = `${newHeight}px`;
    }, []);

    useEffect(() => {
        const textarea = textareaRef.current;
        if (textarea) {
            textarea.style.height = "80px";
        }
    }, []);

    const handleSendMessage = async () => {
        if (!value.trim()) return;

        const userMessage: Message = {
            text: value.trim(),
            sender: 'user',
            timestamp: new Date()
        };

        setMessages(prev => [...prev, userMessage]);
        setValue("");
        adjustHeight(true);

        startTransition(async () => {
            setIsTyping(true);
            
            try {
                const response = await fetch(API_URL, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        user_id: 'web_user_' + Math.random().toString(36).substr(2, 9),
                        session_id: 'web_session_' + Date.now(),
                        message: userMessage.text
                    })
                });

                const data = await response.json();
                
                const botMessage: Message = {
                    text: data.response,
                    sender: 'bot',
                    timestamp: new Date()
                };

                setMessages(prev => [...prev, botMessage]);
            } catch (error) {
                const errorMessage: Message = {
                    text: 'Sorry, I encountered an error. Please try again.',
                    sender: 'bot',
                    timestamp: new Date()
                };
                setMessages(prev => [...prev, errorMessage]);
            } finally {
                setIsTyping(false);
            }
        });
    };

    const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            handleSendMessage();
        }
    };

    const removeAttachment = (index: number) => {
        setAttachments(prev => prev.filter((_, i) => i !== index));
    };

    useEffect(() => {
        if (chatContainerRef.current) {
            chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
        }
    }, [messages]);

    return (
        <div className="min-h-screen flex flex-col w-full items-center justify-center bg-gray-900 text-white p-6">
            <div className="w-full max-w-4xl mx-auto">
                <h1 className="text-3xl font-bold text-center mb-8 bg-gradient-to-r from-blue-400 to-purple-600 bg-clip-text text-transparent">
                    Guardian AI - Cybersecurity Assistant
                </h1>

                <div 
                    ref={chatContainerRef}
                    className="bg-gray-800 rounded-lg p-4 mb-4 h-96 overflow-y-auto space-y-4"
                >
                    {messages.map((message, index) => (
                        <div
                            key={index}
                            className={cn(
                                "flex",
                                message.sender === 'user' ? "justify-end" : "justify-start"
                            )}
                        >
                            <div
                                className={cn(
                                    "max-w-xs px-4 py-2 rounded-lg",
                                    message.sender === 'user' 
                                        ? "bg-blue-600 text-white" 
                                        : "bg-gray-700 text-gray-100"
                                )}
                            >
                                <p className="text-sm">{message.text}</p>
                            </div>
                        </div>
                    ))}

                    {isTyping && (
                        <div className="flex justify-start">
                            <div className="bg-gray-700 text-gray-100 px-4 py-2 rounded-lg">
                                <div className="flex items-center gap-2">
                                    <LoaderIcon className="w-4 h-4 animate-spin" />
                                    <span className="text-sm">Guardian AI is thinking...</span>
                                </div>
                            </div>
                        </div>
                    )}
                </div>

                <div className="bg-gray-800 rounded-lg p-4">
                    <div className="flex gap-2 mb-3">
                        {attachments.map((file, index) => (
                            <div key={index} className="bg-gray-700 px-3 py-1 rounded text-sm flex items-center gap-2">
                                <span>{file}</span>
                                <button 
                                    onClick={() => removeAttachment(index)}
                                    className="text-gray-400 hover:text-white"
                                >
                                    <XIcon className="w-3 h-3" />
                                </button>
                            </div>
                        ))}
                    </div>

                    <div className="flex gap-2">
                        <Textarea
                            ref={textareaRef}
                            value={value}
                            onChange={(e) => {
                                setValue(e.target.value);
                                adjustHeight();
                            }}
                            onKeyDown={handleKeyDown}
                            placeholder="Ask about cybersecurity..."
                            containerClassName="flex-1"
                            className="bg-gray-700 text-white placeholder-gray-400 border-gray-600"
                            showRing={false}
                        />

                        <button
                            onClick={handleSendMessage}
                            disabled={isPending || !value.trim() || isTyping}
                            className={cn(
                                "px-6 py-2 rounded-lg font-medium transition-all",
                                "flex items-center gap-2",
                                value.trim() && !isTyping
                                    ? "bg-blue-600 hover:bg-blue-700 text-white"
                                    : "bg-gray-600 text-gray-400 cursor-not-allowed"
                            )}
                        >
                            {isTyping ? (
                                <LoaderIcon className="w-4 h-4 animate-spin" />
                            ) : (
                                <SendIcon className="w-4 h-4" />
                            )}
                            <span>Send</span>
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
}
```

### 7. Update Main Page
```tsx
// app/page.tsx
import { AnimatedAIChat } from "@/components/ui/animated-ai-chat";

export default function Home() {
  return (
    <main className="min-h-screen">
      <AnimatedAIChat />
    </main>
  );
}
```

### 8. Environment Variables
```bash
# .env.local
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1/chat
```

### 9. Run Development
```bash
npm run dev
```

### 10. Deploy
```bash
# Deploy to Vercel
npm install -g vercel
vercel --prod

# Update API URL in Vercel dashboard to your deployed backend
```

## Integration Notes

1. **API Integration**: Component calls your FastAPI backend
2. **Error Handling**: Shows user-friendly error messages
3. **Real-time**: Typing indicators and smooth animations
4. **Responsive**: Works on all screen sizes
5. **Cybersecurity Focus**: Clean, professional interface

## Required Backend Updates

Add CORS for your frontend domain:
```python
# In main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.vercel.app", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```
