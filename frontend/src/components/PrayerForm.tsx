import { useState } from "react";
import axios, { AxiosError } from "axios";
import { Send } from "lucide-react";
import SuccessCard from "./SucessCard";
import ErrorCard from "./ErrorCard";

interface SuccessResponse {
  detail: {
    type: "success";
    user_message: string;
  };
}

interface ErrorResponse {
  detail: {
    type: "error";
    reason: string;
    limit?: number;
    time_window_seconds?: number;
    retry_after_seconds?: number;
    ban_duration_seconds?: number;
    time_remaining_seconds?: number;
  };
}

type ApiResponse = SuccessResponse | ErrorResponse;

const PrayerForm: React.FC = () => {
  const [message, setMessage] = useState<string>("");
  const [response, setResponse] = useState<ApiResponse | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const MAX_CHARACTERS = 280;

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    // Reset previous response and set loading
    setResponse(null);
    setIsLoading(true);

    try {
      const apiResponse = await axios.post<ApiResponse>(
        "http://localhost:8000/prayers",
        {
          user_message: message,
        }
      );

      // Successful response
      setResponse(apiResponse.data);
    } catch (error) {
      // Error handling for different API error scenarios
      if (axios.isAxiosError(error)) {
        const apiError = error as AxiosError<ErrorResponse>;

        if (apiError.response) {
          setResponse(apiError.response.data);
        } else {
          setResponse({
            detail: { type: "error", reason: "An unexpected error occurred" },
          });
        }
      } else {
        setResponse({
          detail: { type: "error", reason: "An unexpected error occurred" },
        });
      }
    } finally {
      setIsLoading(false);
    }
  };

  // Render method remains similar to previous example
  return (
    <div className="max-w-md mx-auto mt-8">
      <form
        onSubmit={handleSubmit}
        className="bg-gray-800 p-6 rounded-lg shadow-lg"
      >
        <textarea
          value={message}
          onChange={(e: React.ChangeEvent<HTMLTextAreaElement>) =>
            setMessage(e.target.value)
          }
          className="w-full bg-gray-700 text-white p-2 rounded border-none mb-2"
          placeholder="Write your prayer here..."
          rows={4}
          maxLength={MAX_CHARACTERS}
          disabled={isLoading}
        />
        <div className="flex justify-between items-center">
          <span className="text-gray-400">
            {message.length}/{MAX_CHARACTERS}
          </span>
          <button
            type="submit"
            disabled={
              message.length === 0 ||
              message.length > MAX_CHARACTERS ||
              isLoading
            }
            className="bg-blue-600 text-white px-4 py-2 rounded 
                disabled:opacity-50 disabled:cursor-not-allowed 
                hover:bg-blue-700 transition flex items-center gap-2"
          >
            {isLoading ? (
              "Sending..."
            ) : (
              <>
                <Send size={18} /> Send
              </>
            )}
          </button>
        </div>
      </form>

      {response && (
        <div className="mt-4">
          {response.detail.type === "success" ? (
            <SuccessCard message={response.detail.user_message} />
          ) : (
            <ErrorCard message={response.detail.reason} />
          )}
        </div>
      )}
    </div>
  );
};

export default PrayerForm;
