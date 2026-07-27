import React, { useState, forwardRef } from 'react';
import Input, { InputProps } from './Input';
import { Eye, EyeOff, Lock } from 'lucide-react';

const PasswordInput = forwardRef<HTMLInputElement, Omit<InputProps, 'type'>>(
  ({ className = '', ...props }, ref) => {
    const [showPassword, setShowPassword] = useState(false);

    return (
      <div className="relative w-full">
        <Input
          ref={ref}
          type={showPassword ? 'text' : 'password'}
          icon={<Lock className="w-5 h-5" />}
          className={`pr-10 ${className}`}
          {...props}
        />
        <button
          type="button"
          className="absolute inset-y-0 right-0 pr-3 flex items-center text-slate-400 hover:text-slate-600 dark:hover:text-slate-300 focus:outline-none"
          onClick={() => setShowPassword(!showPassword)}
          style={{ top: props.label ? '24px' : '0' }}
        >
          {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
        </button>
      </div>
    );
  }
);

PasswordInput.displayName = 'PasswordInput';
export default PasswordInput;
